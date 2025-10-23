def read_answer(answer: str) -> bool:
    lower_answer = answer.lower().strip()
    if lower_answer in ["no", "false", "n", "f", "no."]:
        return False
    elif lower_answer in ["yes", "true", "yes."]:
        return True

    else:
        if lower_answer.startswith("yes"):
            return True
        elif lower_answer.startswith("no"):
            return False
        else:
            raise ValueError(
                f"Unexpected answer format: {answer}. Expected 'yes' or 'no'."
            )
