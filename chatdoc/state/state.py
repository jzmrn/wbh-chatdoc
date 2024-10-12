import os
from pathlib import Path

import reflex as rx
from langchain.chains import (
    ConversationalRetrievalChain,
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

from chatdoc.constants import UPLOAD_ID

if "PINECONE_API_KEY" not in os.environ:
    raise ValueError("PINECONE_API_KEY is not set.")

if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY is not set.")


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Intros": [],
}


class State(rx.State):
    """The app state."""

    uploading: bool = False
    progress: int = 0

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The name of the new chat.
    new_chat_name: str = ""

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    #########
    # Chats #
    #########

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    @rx.var
    def current_chat_messages(self):
        """Get the messages for the current chat."""
        return self.chats[self.current_chat]

    #######
    # LLM #
    #######

    @rx.var
    def vectordb(self) -> PineconeVectorStore:
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])

        index_name = "langchain-demo"
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                metric="cosine",
                dimension=1536,
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        index = pc.Index(index_name)
        return PineconeVectorStore(index=index, embedding=embeddings)

    @rx.var
    def chain(self) -> ConversationalRetrievalChain:
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0,
            # streaming=True,
            api_key=os.environ["OPENAI_API_KEY"],
        )

        # Contextualize question
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, just "
            "reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            llm, self.vectordb.as_retriever(), contextualize_q_prompt
        )

        # Answer question
        qa_system_prompt = (
            "You are an assistant called chatdoc for question-answering tasks."
            "Use the following pieces of retrieved context to answer the "
            "question. If you don't know the answer, just say that you "
            "don't know. Use three sentences maximum and keep the answer "
            "concise."
            "Context: {context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        # Below we use create_stuff_documents_chain to feed all retrieved context
        # into the LLM. Note that we can also use StuffDocumentsChain and other
        # instances of BaseCombineDocumentsChain.
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        return create_retrieval_chain(history_aware_retriever, question_answer_chain)

    async def openai_process_question_rag(
        self,
        question: str,
    ):
        # result = self.chain().stream({"question": question})
        # response = result["answer"]
        # st.session_state.messages.append({"role": "assistant", "content": response})
        # utils.print_qa(CustomDocChatbot, user_query, response)

        # # to show references
        # for idx, doc in enumerate(result["source_documents"], 1):
        #     filename = os.path.basename(doc.metadata["source"])
        #     page_num = doc.metadata["page"]
        #     ref_title = f":blue[Reference {idx}: *{filename} - page.{page_num}*]"
        #     with st.popover(ref_title):
        #         st.caption(doc.page_content)

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = []
        for qa in self.current_chat_messages:
            messages.append(("user", qa.question))
            messages.append(("ai", qa.answer))

        # Remove the last mock answer.
        messages = messages[:-1]

        session = self.chain.stream({"input": question, "chat_history": messages})
        for item in session:
            if "answer" in item and (delta := item["answer"]) is not None:
                self.chats[self.current_chat][-1].answer += delta
                yield

        # Toggle the processing flag.
        self.processing = False

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        async for value in self.openai_process_question_rag(question):
            yield value

    ##########
    # Upload #
    ##########

    async def handle_upload(self, files: list[rx.UploadFile]):
        self.progress = 0

        folder = "tmp"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # TODO: avoid collisions and delete temporary files
        for file in files:
            print(f"Processing {file.filename}")
            with open(f"./{folder}/{file.filename}", "wb") as f:
                f.write(await file.read())

        TMP_DIR = Path("./tmp")
        loader = DirectoryLoader(TMP_DIR.as_posix(), glob="**/*.pdf")
        documents = loader.load()

        print(f"Loaded {len(documents)} documents.")
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

        print("Splitting documents...")
        chunks = text_splitter.split_documents(documents)

        print("Adding chunks to Pinecone...")
        ids = self.vectordb.add_documents(chunks)
        print("Added documents with IDs:", ids)

    def handle_upload_progress(self, progress: dict):
        self.uploading = True
        self.progress = round(progress["progress"] * 100)
        if self.progress >= 100:
            self.uploading = False

    def cancel_upload(self):
        self.uploading = False
        return rx.cancel_upload(UPLOAD_ID)
