# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

class PHQ9ScreeningAction(Action):
    def name(self) -> Text:
        return "action_screen_phq9"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message["intent"].get("name")

        if intent == "huzuni" or intent == "mawazo":
            # PHQ-9 Questions
            phq9_questions = [
                "kukosa hamu/ari au raha ya kufanya kitu?",
                "kuwa myonge,mwenye huzuni au kukosa matumaini?",
                "Shida ya kupata usingizi,kuamka mapema mno,au kulala mno?",
                "kujisikia kuchoka au mdhaifu wa nguvu ya mwili?",
                "kukosa hamu ya kula au kula sana?",
                "kujisikia vibaya-au ni kwamba umeshashindwa au kukubali kuwa mnyonge wewe na familia yako?",
                "kukosa umakini katika shunguki zako za kawaida kama kusoma gazeti au kuangalia TV?",
                "Kutembea au kuongea kwa pole pole sana hadi watu wengine kutambua,au kinyume chake-kuwa na mahangaiko au kukosa utulivu,kutembea hapa na pale mara nyingi kuliko kawaida yako?",
                "kuwa na mawazo kwamba bora ungekuwa umekufa,au kujidhuru mwenyewe?"
            ]

            # Store user's responses
            responses = tracker.get_slot("phq9_responses")
            if responses is None:
                responses = []
           
            current_question_index = tracker.get_slot("current_question_index")
            if current_question_index is None:
                current_question_index = 0
            else:
                current_question_index += 1

            if current_question_index < len(phq9_questions):
                # Ask the current question and wait for the user's response
                question = phq9_questions[current_question_index]
                dispatcher.utter_message(text=question)

                return [
                    SlotSet("current_question_index", current_question_index),
                    SlotSet("phq9_responses", responses),
                    FollowupAction("action_listen")
                ]
            else:
                # PHQ-9 test is complete

                # PHQ-9 answers
                phq9_answers = {
                    "haijawahi kutokea": 0,
                    "siku kadhaa": 1,
                    "zaidi ya nusu siku": 2,
                    "karibu kila siku": 3
                }

                # Calculate the PHQ-9 score
                phq9_score = sum(responses)

                # Interpret the severity of depression based on the score
                if phq9_score < 5:
                    severity = "unyogovu mdogo"
                elif phq9_score < 10:
                    severity = "unyogovu mpole"
                elif phq9_score < 15:
                    severity = "unyogovu wa wastani"
                else:
                    severity = "unyogovu mkali"

                # Send the result to the user
                dispatcher.utter_message(
                    f"Kulingana na majibu yako kwa dodoso la PHQ-9, alama yako ni {phq9_score}. "
                    f"Hii inaonyesha {severity}. Ni muhimu kushauriana na mtaalamu wa afya ya akili kwa tathmini sahihi zaidi na kujadili chaguzi zinazowezekana za matibabu."
                )

                # Reset the slots
                return [
                    SlotSet("current_question_index", None),
                    SlotSet("phq9_responses", None)
                ]
        else:
            dispatcher.utter_message("Hakuna uchunguzi wa PHQ-9 unaohitajika kwa dhamira hii.")
            return []





class GAD7ScreeningAction(Action):
    def name(self) -> Text:
        return "action_screen_gad7"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message["intent"].get("name")

        if intent == "wasiwasi":
            # GAD-7  Questions
            gad7_questions = [
                "Kujiskia wasiwasi,hofu,wahaka,na hali ya ukali?",
                "kutokuwa na uwezo wa kudhibiti hali ya wasiwasi?",
                "kuwa na wasiwasi sana juu ya mambo mbalimbali?",
                "kupata shida ya utulivu?",
                "kuwa na mahangaiko hadi kuwa ngumu kutulia mahala pamoja?",
                "kuudhika kwa haraka au kuwa mkali?",
                "kujiskia uwoga kama vile jambo baya litatokea?",
            ]
           
            # GAD-7 answers
            gad7_answers = {
                "haijawahi kutokea": 0,
                "siku kadhaa": 1,
                "zaidi ya nusu siku": 2,
                "karibu kila siku": 3
            }
           
            # Store user's responses
            responses = []

            # Administer the GAD-7 test
            for question in gad7_questions:
                dispatcher.utter_message(question)
                response = tracker.latest_message.get("text")
               
                # Map user's answer to a numerical value
                if response in gad7_answers:
                    responses.append(gad7_answers[response])
                else:
                    # Invalid answer, assume it as "Not at all"
                    responses.append(gad7_answers["haijawahi kutokea"])
           
            # Calculate the GAD-7 score
            gad7_score = sum(responses)
           
            # Interpret the severity of depression based on the score
            if gad7_score < 5:
                severity = "wasiwasi mdogo"
            elif gad7_score < 10:
                severity = "wasiwasi mpole"
            elif gad7_score < 15:
                severity = "wasiwasi wa wastani"
            else:
                severity = "wasiwasi mkali"
           
            # Send the result to the user
            dispatcher.utter_message(
                f"Kulingana na majibu yako kwa dodoso la GAD-7, alama yako ni {gad7_score}. "
                f"Hii inaonyesha  {severity}. Ni muhimu kushauriana na mtaalamu wa afya ya akili kwa tathmini sahihi zaidi na kujadili chaguzi zinazowezekana za matibabu."
            )
        else:
            dispatcher.utter_message("Hakuna uchunguzi wa GAD-7 unaohitajika kwa dhamira hii.")

        return []