# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
# Rasa
from rasa_sdk import Action,Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk.events import SlotSet,FollowupAction,UserUtteranceReverted, ConversationPaused

# Helper libraries
import random
import re
from time import time,sleep
from authlib.integrations.requests_client import AssertionSession
from gspread import Client
import json
import requests
import infermedica_api



# Ref:https://blog.authlib.org/2018/authlib-for-gspread
def create_assertion_session(conf_file, subject=None):
    with open(conf_file, 'r') as f:
        conf = json.load(f)

    key_id = conf.get('private_key_id')
    header = {'alg': 'RS256'}
    if key_id:
        header['kid'] = key_id

    scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
    # Google puts scope in payload
    claims = {'scope': ' '.join(scopes)}
    return AssertionSession(
        grant_type=AssertionSession.JWT_BEARER_GRANT_TYPE,
        token_endpoint=conf['token_uri'],
        issuer=conf['client_email'],
        audience=conf['token_uri'],
        claims=claims,
        subject=subject,
        key=conf['private_key'],
        header=header,
    )


# Creating Assersion Session -> requests session
# It will get a valid OAuth token automatically, prepare a requests session for you to use
session = create_assertion_session('basicbot-2f1fe390f8cf.json')
gc = Client(None, session)


# Getting Sheets
ms_sm_wks = gc.open_by_key('').worksheet("intents")
disease_symptom_overview = gc.open_by_key('').worksheet("new_disease_dataframe")

class ActionResponse(Action):
  def name(self) -> Text:
    return "action_response"
  
  def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            dict_of_rec = { "about_treatment":"Lifestyle and home remedies" ,"overveiw": "Overview" ,"causes": "Causes" ,"prevention": "Prevention","about_symptoms": "Symptoms"}

            last_intent = tracker.latest_message['intent'].get('name').split(".")[-1]
            parent_intent = tracker.latest_message['intent'].get('name').split(".")[0]
            disease = tracker.get_slot("disease")
            print(last_intent)
            print(parent_intent)
            intent = tracker.latest_message['intent'].get('name')
            print(intent)
            shan_text = [
                         {
                           "recipient_id": "bot",
                           "type":"text",
                           "text": "Hi again!"
                         }
                        ]
            shan_btn = [
                        {
                           "recipient_id": "bot",
                           "type":"button",
                           "buttons": [
                             {
                               "title": "about products",
                               "payload": "about products"
                             },
                             {
                               "title": "founders of Medsamaan",
                               "payload": "founders of Medsamaan"
                             },
                             {
                               "title": "about Medsamaan",
                               "payload": "about Medsamaan"
                             }
                           ]
                         }
                        ]
            shan_img = [
                        {
                           "recipient_id": "bot",
                           "type":"image",
    
                           "images": [
                             {
                               "text": "about products",
                               "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                             }
                           ]
                         }
                        ]
            
    
            shan_img_btn =[
                          {
                            "recipient_id": "bot",
                            "type" : "image_button",
                            "buttons": [
                              {
                                "title": "about products",
                                "payload": "about products"
                              },
                              {
                                "title": "founders of Medsamaan",
                                "payload": "founders of Medsamaan"
                              },
                              {
                                "title": "about Medsamaan",
                                "payload": "about Medsamaan"
                              }
    
                            ],
                            "images": [
                             {
                               "text": "about products",
                               "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                             },
                             {
                               "text": "founders of Medsamaan",
                               "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                             },
                             {
                               "text": "about Medsamaan",
                               "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                             }
                           ]
                          }
                        ]
            shan_img_btn_txt =[
                          {
                            "recipient_id": "bot",
                            "type" : "image_button_text",
                            "text":"cnocvowecowlcwwobvnw wobwevc nwocwe wowbveviosecewv obfnweof vwovnw vwowf eofefne fefoefqefqefqefoaeflaefne faeoffb ofef",
                            "buttons": [
                              {
                                "title": "about products",
                                "payload": "about products"
                              },
                              {
                                "title": "founders of Medsamaan",
                                "payload": "founders of Medsamaan"
                              },
                              {
                                "title": "about Medsamaan",
                                "payload": "about Medsamaan"
                              }
    
                            ],
                            "images": [
                             {
                               "text": "about products",
                               "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                             },
                             {
                               "text": "founders of Medsamaan",
                               "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                             },
                             {
                               "text": "about Medsamaan",
                               "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                             }
                           ]
                          }
                        ]

            dict_of_rec = { "about_treatment":"Lifestyle and home remedies" ,"overveiw": "Overview" ,"causes": "Causes" ,"prevention": "Prevention","about_symptoms": "Symptoms"}
            
            disease = tracker.get_slot("disease")

            intent = tracker.latest_message['intent'].get('name')
            print(intent)
            if intent == "shantanu_img":
                dispatcher.utter_custom_json(shan_img)
            elif intent == "shantanu_text":
                dispatcher.utter_custom_json(shan_text)

            elif intent == "shantanu_btn":
                dispatcher.utter_custom_json(shan_btn)

            elif intent == "shantanu_img_btn":
                dispatcher.utter_custom_json(shan_img_btn)

            elif intent == "shantanu_text_img_button":
                dispatcher.utter_custom_json(shan_img_btn_txt)          
            elif parent_intent == "smalltalk":
                        wks = ms_sm_wks
                        cell = wks.find(last_intent)
                        ## row & col of search element
                        answer = wks.cell(cell.row, cell.col+3).value
                        ## dispatched answer
                        dispatcher.utter_message(answer)
                        shan_text = [
                                {
                                  "recipient_id": "bot",
                                  "type":"text",
                                  "text": answer
                                }
                                ]
                        dispatcher.utter_custom_json(shan_text)
            elif intent =="prevention":
                        
                        wks = disease_symptom_overview
                        print(disease)
                        cell = wks.find(disease.capitalize())
                        ## row & col of search element
                        answer = wks.cell(cell.row, cell.col+4).value
                        
                        #list_of_rem = list(dict_of_rec.keys()).remove(intent)
                        list_of_rem = list(dict_of_rec.keys())
                        list_of_rem.remove(intent)
                        # dispatcher.utter_message("Overview for " + disease)
                        # dispatcher.utter_message(answer)
                        shan_text = [
                                {
                                  "recipient_id": "bot",
                                  "type":"text",
                                  "text": answer
                                }
                                ]
                        dispatcher.utter_custom_json(shan_text)

                        list_of_buttons = []
                        for i in list_of_rem:
                            temp_dict ={}
                            temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                            temp_dict['payload'] = i +" of "+ disease
                            list_of_buttons.append(temp_dict)
                        shan_text_btn = [
                                {
                                  "recipient_id": "bot",
                                  "type":"text_button",
                                  "text":"Related Topics to Look For:",
                                  "buttons": list_of_buttons
                                }
                                ]
                        dispatcher.utter_custom_json(shan_text_btn)
            elif intent=="about_treatment":
                      wks = disease_symptom_overview
                      cell = wks.find(disease.capitalize())
                      ## row & col of search element
                      answer = wks.cell(cell.row, cell.col+1).value            
                      # dispatcher.utter_message("Treatment for " + disease)
                      # dispatcher.utter_message(answer)
                      list_of_rem = list(dict_of_rec.keys())
                      list_of_rem.remove(intent)
                      shan_text = [
                              {
                                "recipient_id": "bot",
                                "type":"text",
                                "text": answer
                              }
                              ]
                      dispatcher.utter_custom_json(shan_text)

                      list_of_buttons = []
                      for i in list_of_rem:
                          temp_dict ={}
                          temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                          temp_dict['payload'] = i +" of "+ disease
                          list_of_buttons.append(temp_dict)
                      shan_text_btn = [
                              {
                                "recipient_id": "bot",
                                "type":"text_button",
                                "text":"Related Topics to Look For:",
                                "buttons": list_of_buttons
                              }
                              ]
                      dispatcher.utter_custom_json(shan_text_btn)
            elif intent=="prevention":
                      wks = disease_symptom_overview
                      cell = wks.find(disease.capitalize())
                      ## row & col of search element
                      answer = wks.cell(cell.row, cell.col+4).value
                      #list_of_rem = list(dict_of_rec.keys()).remove(intent)
                      list_of_rem = list(dict_of_rec.keys())
                      list_of_rem.remove(intent)
                      # dispatcher.utter_message("Overview for " + disease)
                      # dispatcher.utter_message(answer)
                      shan_text = [
                              {
                                "recipient_id": "bot",
                                "type":"text",
                                "text": answer
                              }
                              ]
                      dispatcher.utter_custom_json(shan_text)

                      list_of_buttons = []
                      for i in list_of_rem:
                          temp_dict ={}
                          temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                          temp_dict['payload'] = i +" of "+ disease
                          list_of_buttons.append(temp_dict)
                      shan_text_btn = [
                              {
                                "recipient_id": "bot",
                                "type":"text_button",
                                "text":"Related Topics to Look For:",
                                "buttons": list_of_buttons
                              }
                              ]
                      dispatcher.utter_custom_json(shan_text_btn)
            elif intent=="about_symptoms":
                              wks = disease_symptom_overview
                              cell = wks.find(disease.capitalize())

                              ## row & col of search element
                              answer = wks.cell(cell.row, cell.col+5).value
                              #list_of_rem = list(dict_of_rec.keys()).remove(intent)
                              list_of_rem = list(dict_of_rec.keys())
                              list_of_rem.remove(intent)
                              # dispatcher.utter_message("Symptoms for " + disease)
                              # dispatcher.utter_message(answer)
                              shan_text = [
                                      {
                                        "recipient_id": "bot",
                                        "type":"text",
                                        "text": answer
                                      }
                                      ]
                              dispatcher.utter_custom_json(shan_text)

                              list_of_buttons = []
                              print(list_of_rem)
                              for i in list_of_rem:
                                  temp_dict ={}
                                  temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                                  temp_dict['payload'] = i +" of "+ disease
                                  list_of_buttons.append(temp_dict)
                              shan_text_btn = [
                                      {
                                        "recipient_id": "bot",
                                        "type":"text_button",
                                        "text":"Related Topics to Look For:",
                                        "buttons": list_of_buttons
                                      }
                                      ]
                              dispatcher.utter_custom_json(shan_text_btn)
            elif intent=="overview":
                          wks = disease_symptom_overview
                          cell = wks.find(disease.capitalize())
                          ## row & col of search element
                          answer = wks.cell(cell.row, cell.col+2).value
                          #list_of_rem = list(dict_of_rec.keys()).remove(intent)
                          list_of_rem = list(dict_of_rec.keys())
                          list_of_rem.remove(intent)
                          # dispatcher.utter_message("Overview for " + disease)
                          # dispatcher.utter_message(answer)
                          shan_text = [
                                  {
                                    "recipient_id": "bot",
                                    "type":"text",
                                    "text": answer
                                  }
                                  ]
                          dispatcher.utter_custom_json(shan_text)

                          list_of_buttons = []
                          for i in list_of_rem:
                              temp_dict ={}
                              temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                              temp_dict['payload'] = i +" of "+ disease
                              list_of_buttons.append(temp_dict)
                          shan_text_btn = [
                                  {
                                    "recipient_id": "bot",
                                    "type":"text_button",
                                    "text":"Related Topics to Look For:",
                                    "buttons": list_of_buttons
                                  }
                                  ]
                          dispatcher.utter_custom_json(shan_text_btn)
            elif intent=="symptom_checker":
                          user_uttered_msg = tracker.latest_message["text"]
                          infermedica_api.configure(app_id='d91c00d6',app_key='50573fae6348390c63e87e7c5b584547')
                          api = infermedica_api.get_api()
                          headers = {           
                              'App-Id': 'd91c00d6',           
                              'App-Key': '50573fae6348390c63e87e7c5b584547',          
                              'Content-Type': 'application/json',         
                          }         
                          data = str({"text":user_uttered_msg})          
                          response = requests.post('https://api.infermedica.com/v2/parse', headers=headers, data=data)         
                          response.text        
                          request = infermedica_api.Diagnosis(sex='male', age=30)        
                          syms = response.json()['mentions']          
                          for i in syms:         
                              request.add_symptom(i['id'], i['choice_id'])         
                          print(request)       
                          # call diagnosis           
                          request = api.diagnosis(request)          
                          request = request.condition
                          for i in request:
                              shan_text = [
                                      {
                                        "recipient_id": "bot",
                                        "type":"text",
                                        "text": i['common_name']+": "+str(i['probability'])
                                      }
                                      ]
                              dispatcher.utter_custom_json(shan_text)                
            elif "locate" in intent:
                      url='https://maps.googleapis.com/maps/api/place/textsearch/json?'# where you will send your requests
                      api_key='AIzaSyDEnYOHrSNCjqfS3dNr_SZnPjMzU8RT5zQ ' #enter your api key generated, if not generated then generate at https://cloud.google.com/maps-platform/?apis=places
                      url2 = 'https://maps.googleapis.com/maps/api/place/details/json?'
                      def maps(search,location):
                          x = []
                          i =0
                          while((x == [] or x==None) and i<10):
                              x=requests.get(url+'query={}&key={}'.format(search.lower()+"+"+"in"+"+"+location.lower(),api_key)).json()['results']
                              i+=1
                          #Extracted 'results' out of the api data  . 'results' would come in json
                          #return(x)
                          if len(x)<1:
                              print("No "+search.lower()+" found at {0}".format(location))
                          # if query invalid then prompt the user to be more general
                          else:
                              RANGE=3 # default 3 results would be displayed . Change accordingly
                              if len(x)<3:RANGE=2
                              if len(x)<2:RANGE=1
                              print("nearest ".format(RANGE) + search.lower() + " locations found at {} :\n".format(location))
                              for i in range(RANGE):
                                  y = None
                                  j = 0
                                  while((y==[] or y=={} or y==None) and j<10):
                                      y = requests.get(url2+'place_id={}&key={}'.format(x[i]['place_id'],api_key)).json()#['formatted_phone_number']#["formatted_phone_number"]
                                      j+=1
                                  if 'result' in y:
                                      shan_text = [
                                      {
                                        "recipient_id": "bot",
                                        "type":"name_descript",
                                        "items": [{"name":x[i]['name'], "descript":x[i]['formatted_address']+"\n"+y['result']['formatted_phone_number']+"\n"+"https://www.google.com/maps/place/?q=place_id:"+x[i]['place_id']}]
                                      }
                                      ]
                                  else:
                                      shan_text = [
                                      {
                                        "recipient_id": "bot",
                                        "type":"name_descript",
                                        "items": [{"name":x[i]['name'], "descript":x[i]['formatted_address']+"\n"+"https://www.google.com/maps/place/?q=place_id:"+x[i]['place_id']}]
                                      }
                                      ]
                                  dispatcher.utter_custom_json(shan_text)
                      loc = tracker.get_slot('current_location')
                      if intent=="locate_clinic":
                        maps("hospital",loc)
                      elif intent=="locate_doctor":
                        maps("doctor",loc)

                                        "text": i['common_name']+":"+i['probability']
                                      }
                                      ]
                              dispatcher.utter_custom_json(shan_text)                
            elif intent=="location_clinic":
                      pass
            elif intent=="causes":
                          wks = disease_symptom_overview
                          cell = wks.find(disease.capitalize())
                          ## row & col of search element
                          answer = wks.cell(cell.row, cell.col+3).value
              
                          
                          # dispatcher.utter_message("Causes for " + disease)
                          # dispatcher.utter_message(answer)
                          shan_text = [
                                  {
                                    "recipient_id": "bot",
                                    "type":"text",
                                    "text": answers
                                  }
                                  ]
                          dispatcher.utter_custom_json(shan_text)
                          #list_of_rem = list(dict_of_rec.keys()).remove(intent)
                          list_of_rem = list(dict_of_rec.keys())
                          list_of_rem.remove(intent)
                          list_of_buttons = []
                          for i in list_of_rem:
                              temp_dict ={}
                              temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                              temp_dict['payload'] = i +" of "+ disease
                              list_of_buttons.append(temp_dict)
                          shan_text_btn = [
                                  {
                                    "recipient_id": "bot",
                                    "type":"text_button",
                                    "text":"Related Topics to Look For:",
                                    "buttons": list_of_buttons
                                  }
                                  ]
                          dispatcher.utter_custom_json(shan_text_btn)
            
            
            
            return []



class ActionTest(Action):
    def name(self) -> Text:
        return "action_test"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message['intent'].get('name')
        print(intent)
        shan_text = [
                     {
                       "recipient_id": "bot",
                       "type":"text",
                       "text": "Hi again!"
                     }
                    ]
        shan_btn = [
                    {
                       "recipient_id": "bot",
                       "type":"button",
                       "buttons": [
                         {
                           "title": "about products",
                           "payload": "about products"
                         },
                         {
                           "title": "founders of Medsamaan",
                           "payload": "founders of Medsamaan"
                         },
                         {
                           "title": "about Medsamaan",
                           "payload": "about Medsamaan"
                         }
                       ]
                     }
                    ]
        shan_img = [
                    {
                       "recipient_id": "bot",
                       "type":"image",

                       "images": [
                         {
                           "text": "about products",
                           "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                         }
                       ]
                     }
                    ]
        

        shan_img_btn =[
                      {
                        "recipient_id": "bot",
                        "type" : "image_button",
                        "buttons": [
                          {
                            "title": "about products",
                            "payload": "about products"
                          },
                          {
                            "title": "founders of Medsamaan",
                            "payload": "founders of Medsamaan"
                          },
                          {
                            "title": "about Medsamaan",
                            "payload": "about Medsamaan"
                          }

                        ],
                        "images": [
                         {
                           "text": "about products",
                           "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                         },
                         {
                           "text": "founders of Medsamaan",
                           "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                         },
                         {
                           "text": "about Medsamaan",
                           "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                         }
                       ]
                      }
                    ]
        shan_img_btn_txt =[
                      {
                        "recipient_id": "bot",
                        "type" : "image_button_text",
                        "text":"cnocvowecowlcwwobvnw wobwevc nwocwe wowbveviosecewv obfnweof vwovnw vwowf eofefne fefoefqefqefqefoaeflaefne faeoffb ofef",
                        "buttons": [
                          {
                            "title": "about products",
                            "payload": "about products"
                          },
                          {
                            "title": "founders of Medsamaan",
                            "payload": "founders of Medsamaan"
                          },
                          {
                            "title": "about Medsamaan",
                            "payload": "about Medsamaan"
                          }

                        ],
                        "images": [
                         {
                           "text": "about products",
                           "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                         },
                         {
                           "text": "founders of Medsamaan",
                           "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                         },
                         {
                           "text": "about Medsamaan",
                           "src": "https://www.drugs.com/mayo/media/ADF419FD-A51A-430C-9C92-5703D91A2733.jpg"
                         }
                       ]
                      }
                    ]


        if intent == "shantanu_img":
            
            dispatcher.utter_custom_json(shan_img)

        elif intent == "shantanu_text":
            dispatcher.utter_custom_json(shan_text)
        
        elif intent == "shantanu_btn":
            dispatcher.utter_custom_json(shan_btn)
        
        elif intent == "shantanu_img_btn":
            dispatcher.utter_custom_json(shan_img_btn)
        
        elif intent == "shantanu_text_img_button":
            dispatcher.utter_custom_json(shan_img_btn_txt)      
   
   
        return []

class ActionSymptoms(Action):
    def name(self) -> Text:
        return "action_symptoms"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            dict_of_rec = { "about_treatment":"Lifestyle and home remedies" ,"overveiw": "Overview" ,"": "Causes" ,"prevention": "Prevention","about_symptoms": "Symptoms"}
            
            disease = tracker.get_slot("disease")

            intent = tracker.latest_message['intent'].get('name')
            #list_of_rem = list(dict_of_rec.keys()).remove(intent)
            list_of_rem = list(dict_of_rec.keys())
            list_of_rem.remove(intent)
            wks = disease_symptom_overview
            cell = wks.find(disease.capitalize())

            ## row & col of search element
            answer = wks.cell(cell.row, cell.col+5).value
            
            # dispatcher.utter_message("Symptoms for " + disease)
            # dispatcher.utter_message(answer)
            shan_text = [
                     {
                       "recipient_id": "bot",
                       "type":"text",
                       "text": answer
                     }
                    ]
            dispatcher.utter_custom_json(shan_text)

            list_of_buttons = []
            for i in list_of_rem:
              
                temp_dict ={}
                temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                temp_dict['payload'] = i +" of "+ disease
                list_of_buttons.append(temp_dict)
            shan_text_btn = [
                    {
                       "recipient_id": "bot",
                       "type":"text_button",
                       "text":"Related Topics to Look For:",
                       "buttons": list_of_buttons
                     }
                    ]
            dispatcher.utter_custom_json(shan_text_btn)

            return []

class ActionResponse(Action):
    def name(self) -> Text:
        return "action_overview"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dict_of_rec = { "about_treatment":"Lifestyle and home remedies" ,"overveiw": "Overview" ,"": "Causes" ,"prevention": "Prevention","about_symptoms": "Symptoms"}
            
            disease = tracker.get_slot("disease")

            intent = tracker.latest_message['intent'].get('name')
            #list_of_rem = list(dict_of_rec.keys()).remove(intent)
            list_of_rem = list(dict_of_rec.keys())
            list_of_rem.remove(intent)

            disease = tracker.get_slot("disease")
            wks = disease_symptom_overview
            cell = wks.find(disease.capitalize())
            ## row & col of search element
            answer = wks.cell(cell.row, cell.col+2).value
            
            # dispatcher.utter_message("Overview for " + disease)
            # dispatcher.utter_message(answer)
            shan_text = [
                     {
                       "recipient_id": "bot",
                       "type":"text",
                       "text": answer
                     }
                    ]
            dispatcher.utter_custom_json(shan_text)

            list_of_buttons = []
            for i in list_of_rem:
                temp_dict ={}
                temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                temp_dict['payload'] = i +" of "+ disease
                list_of_buttons.append(temp_dict)
            shan_text_btn = [
                    {
                       "recipient_id": "bot",
                       "type":"text_button",
                       "text":"Related Topics to Look For:",
                       "buttons": list_of_buttons
                     }
                    ]
            dispatcher.utter_custom_json(shan_text_btn)

            return []

class ActionResponse(Action):
    def name(self) -> Text:
        return "action_treatment"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dict_of_rec = { "about_treatment":"Lifestyle and home remedies" ,"overveiw": "Overview" ,"": "Causes" ,"prevention": "Prevention","about_symptoms": "Symptoms"}
            
            disease = tracker.get_slot("disease")

            intent = tracker.latest_message['intent'].get('name')
            #list_of_rem = list(dict_of_rec.keys()).remove(intent)
            list_of_rem = list(dict_of_rec.keys())
            list_of_rem.remove(intent)

            disease = tracker.get_slot("disease")
            wks = disease_symptom_overview
            cell = wks.find(disease.capitalize())
            ## row & col of search element
            answer = wks.cell(cell.row, cell.col+1).value            
            # dispatcher.utter_message("Treatment for " + disease)
            # dispatcher.utter_message(answer)
            shan_text = [
                     {
                       "recipient_id": "bot",
                       "type":"text",
                       "text": answer
                     }
                    ]
            dispatcher.utter_custom_json(shan_text)

            list_of_buttons = []
            
            for i in list_of_rem:
                
                temp_dict ={}
                
                temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                temp_dict['payload'] = i +" of "+ disease
                list_of_buttons.append(temp_dict)

            
            shan_text_btn = [
                    {
                       "recipient_id": "bot",
                       "type":"text_button",
                       "text":"Related Topics to Look For:",
                       "buttons": list_of_buttons
                     }
                    ]
            dispatcher.utter_custom_json(shan_text_btn)

            return []


class ActionResponse(Action):
    def name(self) -> Text:
        return "action_causes"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dict_of_rec = { "about_treatment":"Lifestyle and home remedies" ,"overveiw": "Overview" ,"": "Causes" ,"prevention": "Prevention","about_symptoms": "Symptoms"}
            
            disease = tracker.get_slot("disease")

            intent = tracker.latest_message['intent'].get('name')
            #list_of_rem = list(dict_of_rec.keys()).remove(intent)
            list_of_rem = list(dict_of_rec.keys())
            list_of_rem.remove(intent)


            disease = tracker.get_slot("disease")
            wks = disease_symptom_overview
            cell = wks.find(disease.capitalize())
            ## row & col of search element
            answer = wks.cell(cell.row, cell.col+3).value
 
            
            # dispatcher.utter_message("Causes for " + disease)
            # dispatcher.utter_message(answer)
            shan_text = [
                     {
                       "recipient_id": "bot",
                       "type":"text",
                       "text": answers
                     }
                    ]
            dispatcher.utter_custom_json(shan_text)

            list_of_buttons = []
            for i in list_of_rem:
                temp_dict ={}
                temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                temp_dict['payload'] = i +" of "+ disease
                list_of_buttons.append(temp_dict)
            shan_text_btn = [
                    {
                       "recipient_id": "bot",
                       "type":"text_button",
                       "text":"Related Topics to Look For:",
                       "buttons": list_of_buttons
                     }
                    ]
            dispatcher.utter_custom_json(shan_text_btn)

            return []


class ActionResponse(Action):
    def name(self) -> Text:
        return "action_prevention"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dict_of_rec = { "about_treatment":"Lifestyle and home remedies" ,"overveiw": "Overview" ,"": "Causes" ,"prevention": "Prevention","about_symptoms": "Symptoms"}
            
            disease = tracker.get_slot("disease")

            intent = tracker.latest_message['intent'].get('name')
            #list_of_rem = list(dict_of_rec.keys()).remove(intent)
            list_of_rem = list(dict_of_rec.keys())
            list_of_rem.remove(intent)


            disease = tracker.get_slot("disease")
            wks = disease_symptom_overview
            cell = wks.find(disease.capitalize())
            ## row & col of search element
            answer = wks.cell(cell.row, cell.col+4).value
            
            # dispatcher.utter_message("Overview for " + disease)
            # dispatcher.utter_message(answer)
            shan_text = [
                     {
                       "recipient_id": "bot",
                       "type":"text",
                       "text": answer
                     }
                    ]
            dispatcher.utter_custom_json(shan_text)

            list_of_buttons = []
            for i in list_of_rem:
                temp_dict ={}
                temp_dict['title'] = disease +" of "+ dict_of_rec[i] 
                temp_dict['payload'] = i +" of "+ disease
                list_of_buttons.append(temp_dict)
            shan_text_btn = [
                    {
                       "recipient_id": "bot",
                       "type":"text_button",
                       "text":"Related Topics to Look For:",
                       "buttons": list_of_buttons
                     }
                    ]
            dispatcher.utter_custom_json(shan_text_btn)

            return []



class ActionResponse(Action):
    def name(self) -> Text:
        return "action_symptoms_checker"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            intent = tracker.latest_message['intent'].get('name')
            user_uttered_msg = tracker.latest_message["text"]
            headers = {           
                'App-Id': 'd91c00d6',           
                'App-Key': '50573fae6348390c63e87e7c5b584547',          
                'Content-Type': 'application/json',         
            }         
            data = str({"text":user_uttered_msg})          
            response = requests.post('https://api.infermedica.com/v2/parse', headers=headers, data=data)         
            response.text        
            request = infermedica_api.Diagnosis(sex='male', age=30)        
            syms = response.json()['mentions']          
            for i in syms:         
                request.add_symptom(i['id'], i['choice_id'])         
            print(request)       
            # call diagnosis           
            request = api.diagnosis(request)          
            request = request.conditions
            print(request)            
            dispatcher.utter_custom_json(request)
            return []

class ActionDefaultAskAffirmation(Action):
   """Asks for an affirmation of the intent if NLU threshold is not met."""

   def name(self):
        return "action_default_ask_affirmation"

   def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_default", tracker)
        return []

class ActionDefaultAskRephrase(Action):
    def name(self) -> Text:
        return "action_default_ask_rephrase"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:
        # Fallback caused by Core
        dispatcher.utter_template("utter_default", tracker)
        return []




class Actionlocation(Action):
    def name(self) -> Text:
        return "action_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:
        # Fallback caused by Core
        location = tracker.get_slot("current_location")
        dispatcher.utter_message(location)
        return []




