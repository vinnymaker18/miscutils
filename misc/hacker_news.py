"""A simple command line tool for reading article titles submitted to
news.ycombinator.com
"""
import HTMLParser


class MyHTMLParser(HTMLParser.HTMLParser):
    """Parses the html text into a dict and returns it.
    """
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.tag_to_data = dict()
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if not self.tag_stack or self.tag_stack[-1] != tag:
            raise ValueError("Invalid html data passed.")

    def handle_data(self, data):
        print "data received is ", data


def main():
    html_text = '<html></html>'
    parser = MyHTMLParser()
    parser.feed(html_text)

if __name__ == '__main__':
    main()
