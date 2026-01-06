from dotenv import load_dotenv
import os
from django.http import JsonResponse
from django.views import View
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from .models import Query
from .utils import vector_store

load_dotenv()

class AnswerQuestion(View):
    def get(self, request):
        question = request.GET.get('q', '')
        if not question:
            return JsonResponse({'error': 'سوالی وارد نشده'}, status=400)

        retrieved_docs = vector_store.similarity_search(question, k=3)

        if not retrieved_docs:
            answer = "متأسفانه بخش مرتبطی در اسناد پیدا نشد."
        else:
            context = "\n\n".join([doc.page_content for doc in retrieved_docs])

            print("\nRetrieved documents:\n")
            for i, doc in enumerate(retrieved_docs):
                print(f"document {i}:\n{doc.page_content}\n")

            llm = init_chat_model("llama-3.1-8b-instant", model_provider="groq")

            prompt = PromptTemplate.from_template(
                "سوال: {question}\n\n"
                "متن‌های مرتبط از اسناد:\n{context}\n\n"
                "پاسخ دقیق، مفید و به زبان فارسی بر اساس متن‌های بالا:"
            )

            chain = prompt | llm
            response = chain.invoke({
                "question": question,
                "context": context
            })
            answer = response.content

        query = Query(question=question, answer=answer)
        query.save()

        return JsonResponse({'answer': answer})
