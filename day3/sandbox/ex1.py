class Book(object):
    # static variables are declared here
    book_count = 0
    def __init__(self, **kwargs):
        Book.book_count += 1
        self.id = Book.book_count
        self.title = kwargs.get('title')
        self.author = kwargs.get('author')

    def __str__(self):
        return f'Book [id={self.id}, title="{self.title}", author="{self.author}"]'


def main():
    b1 = Book(title='Let us C', author='Y Kanitkar')
    # 1. Book() is an instruction to Python RTE to allocate memory for a new object
    # 2. Invoke a method in the class called __init__ by supplying a reference to the newly constructed object
    # 3. we provide a __init__ method to add member variables to the newly constructed object using the parameter given 'self'
    # 4. then the python RTE returns the reference of the newly constructed object, which is then assigned to `b1`
    print(b1)
    b2 = Book(title='Let us Python', author='Vinod')
    print(b2)
    b3 = Book(title = 'Java Unleashed')
    print(b3)
    print(b3.__dict__)


if __name__ == '__main__':
    main()