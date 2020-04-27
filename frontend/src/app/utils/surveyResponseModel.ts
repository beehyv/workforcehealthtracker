export class Question {
  question_id: number;
  answer: string;
  survey_instance_id: string;
  constructor(questionId, answer, surveyId) {
    this.question_id = questionId;
    if (answer === true) {
      this.answer = '1';
    } else if (answer === false) {
      this.answer = '0';
    } else if (answer !== null && answer !== undefined) {
      this.answer = answer.toString();
    } else {
      this.answer = answer;
    }
    this.survey_instance_id = surveyId;
  }
}
