from transformers import pipeline

summarizer = pipeline('summarization')
text = """

The Royal Navy has launched a new training programme to help its naval forces adapt to a new environment. The programme, which will be led by the Royal Navy's Chief Naval Officer, aims to improve the performance of naval forces in the face of increasingly challenging conditions.

The Royal Navy is working with its naval forces to develop new training techniques and equipment to help them adapt to the new environment. The new training programme will be led by the Chief Naval Officer, who will be responsible for overseeing the training process and ensuring that the naval forces are well-prepared for the challenges they will face in the future.        

"""

summary = summarizer(text, max_length=130, min_length=30, do_sample=False)

print(summary[0]["summary_text"])