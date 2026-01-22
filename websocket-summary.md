## Summary

This pull request implements comprehensive WebSocket protocol support following RFC 6455 specification. The implementation includes frame parsing, masking/unmasking, handshake processing, and connection state management with full compliance to the WebSocket standard.

## Changes

- Implement WebSocket protocol handshake and frame handling
- Add support for text, binary, close, ping, and pong frames
- Include proper masking and unmasking for client and server
- Add comprehensive error handling and protocol compliance
- Include unit tests for WebSocket functionality
- Add example usage and documentation

## Implementation Details

The implementation includes:
- WebSocketFrame class for frame parsing/encoding
- WebSocketHandshake class for connection upgrade
- Masking/unmasking functionality per RFC 6455 section 5.3
- Configuration options for WebSocket settings
- Security features like origin validation and frame masking
- Performance benchmarks and test vectors

## Compatibility

- Backward compatible with existing HTTP functionality
- WebSocket support can be disabled via configuration
- Follows RFC 6455 specification exactly

## Testing

All functionality is validated against RFC 6455 test vectors and includes proper error handling for production use.

Closes #123 - Add WebSocket protocol support
Closes #124 - Implement RFC 6455 frame masking
