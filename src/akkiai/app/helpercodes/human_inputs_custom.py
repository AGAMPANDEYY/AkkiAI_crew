import asyncio
import requests

'''
Custom methods for human inputs 
'''

class AgentFinish:
        thought: str
        output: str
        text: str

        def __init__(self, thought: str, output: str, text: str):
            self.thought = thought
            self.output = output
            self.text = text

def _handle_human_feedback(self, formatted_answer: AgentFinish) -> AgentFinish:
    """
    Handles the human feedback loop, allowing the user to provide feedback
    on the agent's output and determining if additional iterations are needed.

    Parameters:
        formatted_answer (AgentFinish): The initial output from the agent.

    Returns:
        AgentFinish: The final output after incorporating human feedback.
    """
    while self.ask_for_human_input:
        human_feedback = self._ask_human_input(formatted_answer.output)

        if self.crew and self.crew._train:
            self._handle_crew_training_output(formatted_answer, human_feedback)

        # Make an LLM call to verify if additional changes are requested based on human feedback
        additional_changes_prompt = self._i18n.slice(
            "human_feedback_classification"
        ).format(feedback=human_feedback)

        retry_count = 0
        llm_call_successful = False
        additional_changes_response = None

        while retry_count < 2 and not llm_call_successful:
            print(f"Retry count set to: {2}")
            try:
                # Fix: Add a 'user' role message as the first message
                messages = [
                    self._format_msg(f"Feedback: {human_feedback}", role="user"),  # First message is user feedback
                    self._format_msg(additional_changes_prompt, role="system")  # System prompt follows
                ]

                # Make the LLM call with the updated messages
                additional_changes_response = (
                    self.llm.call(
                        messages,
                        callbacks=self.callbacks,
                    )
                    .strip()
                    .lower()
                )
                llm_call_successful = True
            except Exception as e:
                retry_count += 1

                self._printer.print(
                    content=f"Error during LLM call to classify human feedback: {e}. Retrying... ({retry_count}/{2})",
                    color="red",
                )

        if not llm_call_successful:
            self._printer.print(
                content="Error processing feedback after multiple attempts.",
                color="red",
            )
            self.ask_for_human_input = False
            break

        if additional_changes_response == "false":
            self.ask_for_human_input = False
        elif additional_changes_response == "true":
            self.ask_for_human_input = True
            # Add human feedback to messages
            self.messages.append(self._format_msg(f"Feedback: {human_feedback}", role="user"))
            # Invoke the loop again with updated messages
            formatted_answer = self._invoke_loop()

            if self.crew and self.crew._train:
                self._handle_crew_training_output(formatted_answer)
        else:
            # Unexpected response
            self._printer.print(
                content=f"Unexpected response from LLM: '{additional_changes_response}'. Assuming no additional changes requested.",
                color="red",
            )
            self.ask_for_human_input = False

    return formatted_answer


def _ask_human_input(self,final_answer:str)->str:
    print(f"## Final Result: {final_answer}")
    print("Waiting for feedback via FastAPI...")

    feedback=None
    feedback_url = "http://127.0.0.1:8000/submit_feedback/"
    while not feedback:
        try:
            response = requests.get(feedback_url)
            if response.status_code == 200:
                feedback_data = response.json()
                feedback = feedback_data.get("feedback", None)
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching feedback: {e}")
        asyncio.sleep(1)
        
    return feedback