class BaseService:
    def __init__(self, llm, prompt_builder, validator, extractor, parser, retry_fn):
        self.llm = llm
        self.prompt_builder = prompt_builder
        self.validator = validator
        self.extract_json = extractor
        self.parse_json = parser
        self.retry = retry_fn

    def execute(self, input_text):
        prompt = self.prompt_builder(input_text)

        for response in self.retry(self.llm, prompt):
            cleaned = self.extract_json(response)
            data = self.parse_json(cleaned)

            if self.validator(data):
                return data

        return self.fallback(input_text)

    def fallback(self, input_text):
        return {
            "input": input_text,
            "error": "Unable to process request"
        }