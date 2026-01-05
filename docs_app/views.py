from dotenv import load_dotenv
import os

from django.http import JsonResponse
from django.views import View
from .models import Document, Query

from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain

load_dotenv()

api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")


class AnswerQuestion(View):
    def get(self, request):
        question = request.GET.get('q', '')
        if not question:
            return JsonResponse({'error': 'No question provided'}, status=400)

        words = question.split()
        results = Document.objects.filter(text__icontains=words[0])
        for word in words[1:]:
            results = results.filter(text__icontains=word)

        context = " ".join([doc.text for doc in results])

        llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.5})
        prompt = PromptTemplate(template=f"Question: {question}\nContext: {context}\nAnswer:",
                                input_variables=["question", "context"])
        chain = LLMChain(llm=llm, prompt=prompt)
        answer = chain.run({"question": question, "context": context})

        query = Query(question=question, answer=answer)
        query.save()

        return JsonResponse({'answer': answer})