import logging
import random

from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk.epr_socket import EPRSocket

logger = logging.getLogger(__name__)

def main(app_config=None, x=0, y=0):
    handler = logging.FileHandler("bob.log", encoding="utf-8")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    epr_pairs = 128

    socket = Socket("bob", "alice", log_config=app_config.log_config)
    epr_socket = EPRSocket("alice")

    conn = NetQASMConnection(
        app_name=app_config.app_name,
        log_config=app_config.log_config,
        epr_sockets=[epr_socket],
    )

    raw_key = []
    apply_h = []

    with conn:
        logger.debug("START")

        # Stage 1: Receiving
        logger.debug("Stage 1: Receiving")
        for i in range(epr_pairs):
            qubit = epr_socket.recv_keep(1)[0]

            if bool(random.randint(0, 1)):
                apply_h.append(True)
                qubit.H()
            else:
                apply_h.append(False)

            m = qubit.measure()
            conn.flush()

            logger.debug(f"Pair {i}; Apply H: {apply_h[-1]}; Measured bit: {m}")
            raw_key.append(int(m))

        logger.debug(f"Raw key: {raw_key}")

        # Stage 2: Sifting
        remote_apply_h = socket.recv_structured().payload
        logger.debug(f"Remote H: {remote_apply_h}")

        logger.debug(f"Local H: {apply_h}")
        socket.send_structured(StructuredMessage("H", apply_h))

        sifted_key = []
        for i, (local_h, remote_h) in enumerate(zip(apply_h, remote_apply_h)):
            if local_h == remote_h:
                sifted_key.append(raw_key[i])

        logger.debug(f"Sifted key: {sifted_key}")

        # Stage 3: Security
        num_security_bits = max(len(sifted_key) // 4, 1)
        assert num_security_bits > 0

        security_bits = sifted_key[:num_security_bits]

        remote_security_bits = socket.recv_structured().payload
        logger.debug(f"Remote security bits: {remote_security_bits}")

        logger.debug(f"Local security bits: {security_bits}")
        socket.send_structured(StructuredMessage("Security bits", security_bits))

        if security_bits != remote_security_bits:
            logger.warning("Eavesdropper detected!")
            key = None
        else:
            key = sifted_key[num_security_bits:]

        logger.debug(f"Final key: {key}")

    return {"key": key}


if __name__ == "__main__": 
    main()
