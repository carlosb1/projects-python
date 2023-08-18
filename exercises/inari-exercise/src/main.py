from controller import CodeMaker

DEBUG = True

if __name__ == '__main__':
    SIZE_TO_SEARCH = 4
    NUM_TRIES = 10
    codemaker = CodeMaker.makeCodeMaker(SIZE_TO_SEARCH, NUM_TRIES)
    finish = False
    while not finish:
        finish = codemaker.run()
        if DEBUG:
            print("tries: " + str(codemaker._game.tries))
            print("to search: " + str(codemaker._game.value_to_find))
