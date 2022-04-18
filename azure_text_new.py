def returnMedDict(text, nlp_qa, client, value_dict):
    poller = client.begin_analyze_healthcare_entities(text)
    result = poller.result()
    docs = [doc for doc in result if not doc.is_error]
    for doc in docs:
        for entity in doc.entities:
            if entity.category=='Age':
                value_dict['Age'].append(entity.text)
            elif entity.category=='Gender':
                value_dict['Gender'].append(entity.text)
            elif entity.category=='SymptomOrSign':
                value_dict['Symptoms/sign'].append(entity.text)
        
        for relation in doc.entity_relations:
            # print(f"Relation of type: {relation.relation_type} has the following roles")
            if relation.relation_type=='TimeOfCondition':
                for role in relation.roles:
                    if role.name =='Time':
                        value_dict['Time since the start of the condition'].append(role.entity.text)

            elif relation.relation_type=='ExaminationFindsCondition':
                for role in relation.roles:
                    if role.name =='Examination':
                        value_dict['Examination for condition'].append(role.entity.text)

            elif relation.relation_type=='BodySiteOfCondition' or relation.relation_type=='QualifierOfCondition':
                sent = ''
                for role in relation.roles:
                    sent += role.entity.text + ':'
                value_dict['Medical condition'].append(sent[:-1])
            
            elif relation.relation_type=='DirectionOfBodyStructure':
                sent = ''
                for role in relation.roles:
                    sent = role.entity.text + ':'+ sent
                value_dict['Body structure and direction affected'].append(sent[:-1])
            
            elif relation.relation_type=='CourseOfCondition':
                sent = ''
                for role in relation.roles:
                    sent += role.entity.text + ':'
                value_dict['Course of condition'].append(sent[:-1])
            
            elif relation.relation_type=='CourseOfCondition':
                sent = ''
                for role in relation.roles:
                    sent += role.entity.text + ':'
                value_dict['Course of condition'].append(sent[:-1])
            
            elif relation.relation_type=='TimeOfExamination':
                sent = ''
                for role in relation.roles:
                    sent += role.entity.text + ':'
                value_dict['Time of examination'].append(sent[:-1])
            
            elif relation.relation_type=='FormOfMedication':
                sent = ''
                for role in relation.roles:
                    sent += role.entity.text + ':'
                value_dict['Medication'][0]['Name'].append(sent[:-1])
            elif relation.relation_type=='DosageOfMedication':
                sent = ''
                for role in relation.roles:
                    sent = role.entity.text + ':'+sent
                value_dict['Medication'][0]['Dosage'].append(sent[:-1])
            elif relation.relation_type=='FrequencyOfMedication':
                sent = ''
                for role in relation.roles:
                    sent += role.entity.text + ':'
                value_dict['Medication'][0]['Frequency'].append(sent[:-1])
            elif relation.relation_type=='TimeOfMedication':
                sent = ''
                for role in relation.roles:
                    sent += role.entity.text + ':'
                value_dict['Medication'][0]['Time'].append(sent[:-1])

    y = nlp_qa({'question':'What is the occupation?', 'context':text[0]})
    if y['score'] >=0.6:
        value_dict['Occupation'].append(y['answer'])

    y = nlp_qa({'question':"What is the patient's name?", 'context':text[0]})
    if y['score'] >=0.6:
        value_dict['Name'].append(y['answer'])
    
    y = nlp_qa({'question':"Does the patient smoke?", 'context':text[0]})
    if y['score'] >=0.6:
        value_dict['Personal History'][0]['Smoking'].append('Yes')
    else:
        value_dict['Personal History'][0]['Smoking'].append('No')
    
    y = nlp_qa({'question':"Does the patient drink?", 'context':text[0]})
    if y['score'] >=0.6:
        value_dict['Personal History'][0]['Drinking'].append('Yes')
    else:
        value_dict['Personal History'][0]['Drinking'].append('No')
    
    y = nlp_qa({'question':"Has the patient undergone any tooth extraction or oral procedure?", 'context':text[0]})
    if y['score'] >=0.6:
        value_dict['Dental History'][0]['Previous tooth extraction or oral procedure'].append('Yes')
    else:
        value_dict['Dental History'][0]['Previous tooth extraction or oral procedure'].append('No')
    

    y = nlp_qa({'question':"Does the patient suffer from Asthma?", 'context':text[0]})
    if y['score'] >=0.6:
        value_dict['Medical History'][0]['Asthma'].append('Yes')
    else:
        value_dict['Medical History'][0]['Asthma'].append('No')

    y = nlp_qa({'question':"Has the patient undergone any surgery?", 'context':text[0]})
    if y['score'] >=0.6:
        value_dict['Medical History'][0]['Surgeries'].append('Yes')
    else:
        value_dict['Medical History'][0]['Surgeries'].append('No')
    
    y = nlp_qa({'question':"Has the patient suffered from any bleeding issue?", 'context':text[0]})
    if y['score'] >=0.6:
        value_dict['Medical History'][0]['Bleeding issues'].append('Yes')
    else:
        value_dict['Medical History'][0]['Bleeding issues'].append('No')

    if value_dict['Examination for condition']==[]:
        list1 = []
        for val in value_dict['Time of examination']:
            list1.append(val.split(':')[0])
        value_dict['Examination for condition'].extend(list1)
    # return json.dumps(value_dict, indent = 4)
    return value_dict
                
