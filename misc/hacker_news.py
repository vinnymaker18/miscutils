"""A simple command line tool for reading article titles submitted to
news.ycombinator.com
"""
import HTMLParser


class HTMLData:
    """Represents any piece of data within the body, typically piece of
    text, script/style elements.
    """
    #TODO(vinay) - Expand this class to hold script/style elements as well.
    def __init__(self, data):
        self.data = data


class HTMLNode:
    """Represents an html tag along with any attributes.
    """
    def __init__(self, tag, attrs=None):
        self._children = []
        self._tag = tag
        self._attrs = attrs

    def add_child_node(self, html_node):
        """Adds a sub node to the children list.
        """
        self._children.append(html_node)

    def add_data_piece(self, data):
        """Add a piece of data to this node."""
        self._children.append(data)

    def get_tag(self):
        """Returns the tag name"""
        return self._tag

    def get_attrs(self):
        """Returns the attributes of this tag, if any"""
        return self._attrs

    #TODO(vinay) - Make this a dict-like object.


# Maintains a stack of HTMLNodes as it parses through
class MyHTMLParser(HTMLParser.HTMLParser):
    """Parses the html text into a dict and returns it.
    """

    # Parser states
    PARSE_NOT_YET_STARTED = 0
    PARSE_RUNNING = 1
    PARSE_FAILED = 2
    PARSE_SUCCESS = 3
    PARSE_OTHER = 4

    # Creates a node stack for parsing.
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)

        self.node_stack = []
        self.root_node = None
        self.parse_state = MyHTMLParser.PARSE_NOT_YET_STARTED

    def handle_starttag(self, tag, attrs):
        """Pushes a new node onto the node stack."""
        # set the parsing state to running.
        self.parse_state = MyHTMLParser.PARSE_RUNNING

        cur_node = HTMLNode(tag, attrs)

        if not self.root_node:
            self.root_node = cur_node
        # We've encountered a starting tag,
        self.node_stack.append(cur_node)

    # Checks if this tag matches the last pushed starting tag and
    # pops a node off the stack.
    def handle_endtag(self, tag):
        if not self.node_stack or self.node_stack[-1].get_tag() != tag:
            raise ValueError("Ill-formed html data, aborting")

        # This closing tag matches the last seen starting tag.
        cur_node = self.node_stack.pop()
        if self.node_stack:
            # push this current node into it's parent.
            parent_node = self.node_stack[-1]
            parent_node.add_node(cur_node)
        else:
            # This must be the root node
            self.parse_state = MyHTMLParser.PARSE_SUCCESS

    # Adds a piece of data to the containing node.
    def handle_data(self, data):
        if not self.node_stack:
            raise ValueError("Ill formed html data - aborting.")

        cur_node = self.node_stack[-1]
        cur_node.add_data_piece(data)

    def close(self):
        if self.tag_stack:
            raise ValueError("Ill formed html, aborting")
        # After this, this will have a fully parsed html object.
        self.parse_state = MyHTMLParser.PARSE_SUCCESS
        HTMLParser.HTMLParser.close()

    def get_html_contents(self):
        """Should be called after the html content is fed into this parser.
        Returns the root HTML node.
        """
        return self.root_node


# Goes through a list of html files and tries to parse and print them.
def main():
    html_text = '<html>Some piece of data</html>'
    parser = MyHTMLParser()
    parser.feed(html_text)
    print parser.get_html_contents()


if __name__ == '__main__':
    main()
