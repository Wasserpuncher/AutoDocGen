import os
import ast
from pydoc import render_doc

class DocumentationGenerator:
    def __init__(self, project_path):
        self.project_path = project_path
        self.docs = []

    def generate_docs(self):
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith('.py'):
                    self._generate_doc_for_file(os.path.join(root, file))
        return self.docs

    def _generate_doc_for_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            tree = ast.parse(content, filename=file_path)
            docstring = ast.get_docstring(tree)
            self.docs.append({
                'file': file_path,
                'docstring': docstring,
                'rendered': render_doc(tree)
            })

    def save_docs_as_html(self, output_dir='docs'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for doc in self.docs:
            file_name = os.path.basename(doc['file']).replace('.py', '.html')
            with open(os.path.join(output_dir, file_name), 'w') as file:
                file.write(f"<h1>Documentation for {doc['file']}</h1>")
                file.write(f"<pre>{doc['rendered']}</pre>")

if __name__ == "__main__":
    project_path = 'path/to/your/project'
    doc_generator = DocumentationGenerator(project_path)
    doc_generator.generate_docs()
    doc_generator.save_docs_as_html()
