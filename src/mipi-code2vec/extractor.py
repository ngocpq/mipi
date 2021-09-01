import subprocess


class Extractor:
    def __init__(self, config, jar_path, max_path_length, max_path_width):
        self.config = config
        self.max_path_length = max_path_length
        self.max_path_width = max_path_width
        self.jar_path = jar_path

    def extract_paths_file(self, path):
        command = ['java', '-cp', self.jar_path, 'JavaExtractor.App', '--max_path_length',
                   str(self.max_path_length), '--max_path_width', str(self.max_path_width), '--file', path, '--no_hash']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        output = out.decode().splitlines()
        if len(output) == 0:
            err = err.decode()
            raise ValueError(err)
        hash_to_string_dict = {}
        result = []
        for i, line in enumerate(output):
            parts = line.rstrip().split(' ')
            method_name = parts[0]
            current_result_line_parts = [method_name]
            contexts = parts[1:]
            for context in contexts[:self.config.MAX_CONTEXTS]:
                context_parts = context.split(',')
                context_word1 = context_parts[0]
                context_path = context_parts[1]
                context_word2 = context_parts[2]
                hashed_path = str(self.java_string_hashcode(context_path))
                hash_to_string_dict[hashed_path] = context_path
                current_result_line_parts += ['%s,%s,%s' % (context_word1, hashed_path, context_word2)]
            space_padding = ' ' * (self.config.MAX_CONTEXTS - len(contexts))
            result_line = ' '.join(current_result_line_parts) + space_padding
            result.append(result_line)
        return result, hash_to_string_dict

    def extract_paths_code(self, code):
        code_bytes = code.encode("UTF-8")
        command = ['java', '-cp', self.jar_path, 'JavaExtractor.App', '--max_path_length',
                   str(self.max_path_length), '--max_path_width', str(self.max_path_width), '--stdin', '--no_hash',
                   '--javadoc_print']
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(input=code_bytes)
        output = out.decode().splitlines()
        if len(output) == 0:
            err = err.decode()
            raise ValueError(err)
        hash_to_string_dict = {}
        result = []
        result_texts = []

        for i, line in enumerate(output):
            parts = line.rstrip().split(' ')
            method_name = parts[0]
            if '@' in method_name:
                text_parts = method_name.split('@', 1)
                method_name = text_parts[0]
                description = text_parts[1]
            else:
                description = ""

            current_result_line_parts = [method_name]
            contexts = parts[1:]
            for context in contexts[:self.config.MAX_CONTEXTS]:
                context_parts = context.split(',')
                context_word1 = context_parts[0]
                context_path = context_parts[1]
                context_word2 = context_parts[2]
                hashed_path = str(self.java_string_hashcode(context_path))
                hash_to_string_dict[hashed_path] = context_path
                current_result_line_parts += ['%s,%s,%s' % (context_word1, hashed_path, context_word2)]
            space_padding = ' ' * (self.config.MAX_CONTEXTS - len(contexts))
            result_line = ' '.join(current_result_line_parts) + space_padding
            result.append(result_line)
            result_texts.append(description)
        return result, hash_to_string_dict, result_texts

    @staticmethod
    def java_string_hashcode(s):
        """
        Imitating Java's String#hashCode, because the model is trained on hashed paths but we wish to
        Present the path attention on un-hashed paths.
        """
        h = 0
        for c in s:
            h = (31 * h + ord(c)) & 0xFFFFFFFF
        return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000
