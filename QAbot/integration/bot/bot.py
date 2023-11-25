from django.conf import settings
from operator import itemgetter
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain import hub

from integration.rag_services.knowledge_service import KnowledgeBase
from integration.utils import resolve_file_type


class Bot:
    #  a bot which takes context and questions and returns an answer list

    def __init__(self, temperature=0.6) -> None:
        self.knowledge_base = KnowledgeBase()
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                               temperature=temperature,
                                 openai_api_key=settings.OPENAI_API_KEY)

        self.prompt = hub.pull("rlm/rag-prompt")

        self.chain = {"question": itemgetter("question"), "context": itemgetter("context"),} | \
        self.prompt | \
        self.llm | \
        StrOutputParser()

    def _format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def answer_question(self, question):
        #  get relevant context
        context = self._format_docs(self.knowledge_base.retrive(question=question, top_n=3))
        return self.chain.invoke({'context': context, 'question': question})

    def answer(self, context, questions):
        """
        Args:
            context: path to context file
            questions: a list of questions
        """
        #  add context to knowledge base
        self.knowledge_base.add_document(context, type=resolve_file_type(context))

        answer_dict = {}
        for question in questions:
            answer_dict[question] = self.answer_question(question)

        self.knowledge_base.clean_slate()
        return answer_dict
