def get_input():
    global velocity, vx

    events = XEvents()
    events.start()

    while not events.listening():
        # Wait for init
        time.sleep(1)

    try:
        while events.listening():
            evt = events.next_event()
            # if (evt is not None): debug(evt.get_value())
            if not evt:
                if (velocity > 0): velocity -= vx
                # time.sleep(DELAY)
                continue

            velocity += vx

    except KeyboardInterrupt:
        events.stop_listening()
