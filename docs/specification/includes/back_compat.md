Implementations SHOULD ensure backward compatibility. To achieve backward compatibility, the implementation MUST be able to read all messages from the previous releases of the protocol with the same MAJOR version. The implementation MAY also be able to read messages from previous releases of the protocol with a different MAJOR version.

!!! note

    The protocol is designed in such a way that you don't need to worry about backward compatibility. The only thing you need to do is to implement the latest version of the protocol, and you will automatically get backward compatibility with all previous versions (of the same MAJOR).