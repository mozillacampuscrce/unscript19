import json

with open('questionDoctorQAs.json','r') as f:
	qa_dict = json.load(f)
final = []
que = []
for doc in qa_dict:
	qa_pair = []
	qa_pair.append("<category><pattern>" +str(doc['question']).upper()+"</pattern><template>"+doc['answer']+"</template></category>")
	string = str(doc['question']).upper()
	if string not in que:
		que.append(string)
		if qa_pair not in final:
			final.append(qa_pair)

with open('medical.txt','w', encoding="utf-8") as temp:
	for i in range(0,len(final)):
		temp.write(str(final[i])+"\n");