import threading

def input_with_timeout(prompt, timeout):
    user_input = [None]  # Use a mutable object to store the input

    def get_input():
        user_input[0] = input(prompt)

    # Start a thread to get input
    thread = threading.Thread(target=get_input)
    thread.start()
    thread.join(timeout)  # Wait for the thread to finish or timeout

    if thread.is_alive():
        # If the thread is still running, input timed out
        print("\nInput timed out!")
        thread.join()  # Clean up the thread if necessary
        return 'n'

    return user_input[0]