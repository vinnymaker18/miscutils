"""A simple command line tool for reading article titles submitted to
news.ycombinator.com
"""
import HTMLParser


class MyHTMLParser(HTMLParser.HTMLParser):
    """Parses the html text into a dict and returns it.
    """
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.tag_to_data = dict()
        self.tag_stack = []
        self.current_data = None

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if not self.tag_stack or self.tag_stack[-1] != tag:
            raise ValueError("Invalid html data passed.")

        tag = self.tag_stack.pop()
        if self.current_data:
            self.tag_to_data[tag] = self.current_data
            self.current_data = None
        
    def handle_data(self, data):
        self.current_data = data

    def get_html_contents(self):
        """Should be called after the html content is fed into this parser.
        """
        return self.tag_to_data 


def main():
    html_text = "<html><head><title>Simple text</title></head>\
         <body>Data</body></html>"
    parser = MyHTMLParser()
    parser.feed(html_text)
    html_contents = parser.get_html_contents()
    print html_contents

if __name__ == '__main__':
    main()
