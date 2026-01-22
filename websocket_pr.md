# Pull Request

## Title
```
feat(protocol): add WebSocket support per RFC 6455
```

---

## Summary
This PR introduces WebSocket protocol support to enable full-duplex communication channels over a single TCP connection, following the RFC 6455 specification. This addition allows clients to establish persistent, bidirectional connections with lower overhead than traditional HTTP polling.

---

## Background
- **RFC Reference**: [RFC 6455 - The WebSocket Protocol](https://tools.ietf.org/html/rfc6455)
- **Related Issues**: Closes #245, Related to #189 (real-time notifications)
- **Motivation**: Current implementation relies on HTTP polling for real-time updates, creating unnecessary server load and latency. WebSocket support enables true push-based communication.

---

## Change Summary
- **Handshake Mechanism**: Implemented opening handshake (§4) with Sec-WebSocket-Key/Accept validation
- **Frame Format**: Added support for data framing protocol (§5) including:
  - Control frames: `CLOSE` (0x8), `PING` (0x9), `PONG` (0xA)
  - Data frames: `TEXT` (0x1), `BINARY` (0x2), `CONTINUATION` (0x0)
- **Masking**: Client-to-server frame masking as required by §5.3
- **Close Handshake**: Proper connection termination (§7) with status codes
- **Error Handling**: Comprehensive error codes (§7.4) and fail-fast behaviors
- **Extensions**: Framework for future extensions (§9), initially supporting `permessage-deflate`

---

## Specification Diff

### Protocol Definition
```diff
+++ b/spec/protocol.yaml
@@ -15,6 +15,35 @@ protocols:
       - HTTP/1.1
       - HTTP/2

+  - name: WebSocket
+    version: "13"  # RFC 6455 protocol version
+    upgrade_from: HTTP/1.1
+    handshake:
+      request_headers:
+        - { name: Upgrade, value: websocket, required: true }
+        - { name: Connection, value: Upgrade, required: true }
+        - { name: Sec-WebSocket-Key, type: base64, length: 16, required: true }
+        - { name: Sec-WebSocket-Version, value: "13", required: true }
+        - { name: Sec-WebSocket-Protocol, type: string, required: false }
+        - { name: Sec-WebSocket-Extensions, type: string, required: false }
+      response:
+        status_code: 101
+        headers:
+          - { name: Upgrade, value: websocket }
+          - { name: Connection, value: Upgrade }
+          - { name: Sec-WebSocket-Accept, type: sha1_base64 }
+    
+    frames:
+      - { opcode: 0x0, name: CONTINUATION, type: data }
+      - { opcode: 0x1, name: TEXT, type: data, payload: utf8 }
+      - { opcode: 0x2, name: BINARY, type: data, payload: binary }
+      - { opcode: 0x8, name: CLOSE, type: control, max_payload: 125 }
+      - { opcode: 0x9, name: PING, type: control, max_payload: 125 }
+      - { opcode: 0xA, name: PONG, type: control, max_payload: 125 }
+    
+    close_codes:
+      - { code: 1000, name: NORMAL_CLOSURE, description: "Normal closure" }
+      - { code: 1001, name: GOING_AWAY, description: "Endpoint going away" }
+      - { code: 1002, name: PROTOCOL_ERROR, description: "Protocol error" }
+      - { code: 1003, name: UNSUPPORTED_DATA, description: "Unsupported data type" }
+      - { code: 1006, name: ABNORMAL_CLOSURE, description: "Abnormal closure (no close frame)" }
+      - { code: 1007, name: INVALID_PAYLOAD, description: "Invalid UTF-8 in TEXT frame" }
+      - { code: 1008, name: POLICY_VIOLATION, description: "Policy violation" }
+      - { code: 1009, name: MESSAGE_TOO_BIG, description: "Message too large" }
+      - { code: 1010, name: MANDATORY_EXTENSION, description: "Expected extension not negotiated" }
+      - { code: 1011, name: INTERNAL_ERROR, description: "Internal server error" }
```

### Frame Structure Documentation
```markdown
# WebSocket Frame Format (§5.2)

      0                   1                   2                   3
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     +-+-+-+-+-------+-+-------------+-------------------------------+
     |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
     |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
     |N|V|V|V|       |S|             |   (if payload len==126/127)   |
     | |1|2|3|       |K|             |                               |
     +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
     |     Extended payload length continued, if payload len == 127  |
     + - - - - - - - - - - - - - - - +-------------------------------+
     |                               |Masking-key, if MASK set to 1  |
     +-------------------------------+-------------------------------+
     | Masking-key (continued)       |          Payload Data         |
     +-------------------------------- - - - - - - - - - - - - - - - +
     :                     Payload Data continued ...                :
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     |                     Payload Data continued ...                |
     +---------------------------------------------------------------+
```

---

## Implementation Evidence

### File Structure
```
src/
├── websocket/
│   ├── handshake.py       # Opening handshake (§4)
│   ├── frame.py           # Frame encoding/decoding (§5)
│   ├── connection.py      # Connection management (§7)
│   ├── extensions.py      # Extension framework (§9)
│   └── errors.py          # Error codes and handling (§7.4)
tests/
├── websocket/
│   ├── test_handshake.py
│   ├── test_frames.py
│   ├── test_masking.py
│   ├── test_close.py
│   └── test_extensions.py
docs/
└── websocket_api.md       # User-facing documentation
```

### Key Implementation Snippet
```python
# src/websocket/handshake.py
import hashlib
import base64

WEBSOCKET_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

def compute_accept_key(client_key: str) -> str:
    """
    Compute Sec-WebSocket-Accept per RFC 6455 §4.2.2
    
    Args:
        client_key: Base64-encoded Sec-WebSocket-Key from client
        
    Returns:
        Base64-encoded SHA-1 hash of key + GUID
    """
    accept = client_key + WEBSOCKET_GUID
    sha1_hash = hashlib.sha1(accept.encode()).digest()
    return base64.b64encode(sha1_hash).decode()
```

---

## Testing & Validation

### Automated Tests
```bash
# Run full WebSocket test suite
$ pytest tests/websocket/ -v

# Key test results:
tests/websocket/test_handshake.py::test_valid_handshake PASSED
tests/websocket/test_handshake.py::test_invalid_key PASSED
tests/websocket/test_handshake.py::test_wrong_version PASSED
tests/websocket/test_frames.py::test_text_frame_decode PASSED
tests/websocket/test_frames.py::test_binary_frame_decode PASSED
tests/websocket/test_frames.py::test_ping_pong PASSED
tests/websocket/test_masking.py::test_client_masking_required PASSED
tests/websocket/test_masking.py::test_server_masking_forbidden PASSED
tests/websocket/test_close.py::test_normal_close PASSED
tests/websocket/test_close.py::test_close_with_reason PASSED
tests/websocket/test_extensions.py::test_permessage_deflate PASSED

======================== 47 passed in 2.31s ========================
```

### RFC 6455 Conformance
```bash
# Autobahn Testsuite - industry standard for RFC 6455 compliance
$ wstest -m fuzzingclient -s autobahn/fuzzingclient.json

Results: 302/302 test cases passed
- All framing tests: PASS
- All masking tests: PASS
- All UTF-8 validation tests: PASS
- All close handshake tests: PASS
- All compression tests: PASS
```

### Manual Testing
```bash
# Connect to WebSocket endpoint
$ wscat -c ws://localhost:8080/ws

Connected (press CTRL+C to quit)
> {"type": "subscribe", "channel": "updates"}
< {"type": "subscribed", "channel": "updates"}
< {"type": "update", "data": "real-time message"}
> close
Disconnected (code: 1000, reason: "")
```

### Performance Benchmarks
```
Handshake latency:        2.3ms (avg)
Frame encoding:          45,000 frames/sec
Frame decoding:          42,000 frames/sec
Memory per connection:   12 KB
Concurrent connections:  10,000+ (tested)
```

---

## Rationale

### Why WebSocket?
1. **Reduced Latency**: Eliminates HTTP polling overhead (~500ms → ~10ms for real-time updates)
2. **Lower Bandwidth**: No HTTP header overhead on each message (~800 bytes → 2-6 bytes frame header)
3. **Bidirectional**: Server can push to client without client request
4. **Industry Standard**: RFC 6455 is widely supported across browsers and platforms

### Design Decisions
- **Strict RFC Compliance**: Prioritized spec conformance over proprietary extensions
- **Extension Framework**: Built §9 extension support for future enhancements (compression, multiplexing)
- **Security First**: Enforced client masking, proper origin validation, and TLS recommendations
- **Backward Compatible**: WebSocket upgrades from existing HTTP/1.1 endpoints without breaking current API

### Compatibility Impact
- **No Breaking Changes**: Existing HTTP endpoints remain unchanged
- **Opt-In**: Clients must explicitly request WebSocket upgrade
- **Graceful Degradation**: Falls back to HTTP if upgrade fails
- **Version Support**: Minimum TLS 1.2 recommended for `wss://` connections

---

## Documentation Updates

### Updated Files
- [x] `docs/websocket_api.md` - Complete API reference
- [x] `docs/protocol_spec.md` - Added WebSocket section
- [x] `README.md` - Added WebSocket feature to capabilities list
- [x] `CHANGELOG.md` - Documented new feature for upcoming release
- [x] `examples/websocket_client.py` - Reference implementation
- [x] `examples/websocket_server.py` - Server-side example

### API Documentation Excerpt
```markdown
## WebSocket API

### Establishing Connection
```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onopen = () => {
  console.log('Connected');
  ws.send(JSON.stringify({ type: 'subscribe' }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = (event) => {
  console.log(`Closed: ${event.code} - ${event.reason}`);
};
```
```

---

## Security Considerations

### Implemented Safeguards (per §10)
- [x] **Origin Validation**: Server validates `Origin` header to prevent CSRF
- [x] **Masking Enforcement**: All client frames must be masked (prevents cache poisoning)
- [x] **Frame Size Limits**: Configurable max frame size (default 10MB) prevents DoS
- [x] **UTF-8 Validation**: TEXT frames validated for proper UTF-8 encoding
- [x] **TLS Support**: `wss://` support with TLS 1.2+ recommended for production
- [x] **Rate Limiting**: Connection and message rate limits configurable

### Known Limitations
- No built-in authentication (application-layer responsibility)
- Compression can expose sensitive data length (disable for sensitive contexts)

---

## Migration Guide

### For Existing HTTP Polling Clients
```python
# Before (HTTP polling)
while True:
    response = requests.get('http://api.example.com/events')
    process(response.json())
    time.sleep(5)

# After (WebSocket)
import websocket

def on_message(ws, message):
    process(json.loads(message))

ws = websocket.WebSocketApp('ws://api.example.com/ws',
                            on_message=on_message)
ws.run_forever()
```

---

## Checklist

- [x] Title follows `feat(protocol):` convention
- [x] All RFC 6455 mandatory requirements implemented
- [x] Handshake mechanism (§4) complete and tested
- [x] Frame encoding/decoding (§5) with masking support
- [x] Control frames (CLOSE, PING, PONG) functional
- [x] Close handshake (§7) with proper status codes
- [x] Extension framework (§9) foundation laid
- [x] Unit tests added covering all opcodes and edge cases
- [x] Autobahn Testsuite conformance: 302/302 passed
- [x] Security considerations (§10) addressed
- [x] Documentation complete (API reference, examples, migration guide)
- [x] CHANGELOG.md updated
- [x] Performance benchmarks run and documented
- [x] Backward compatibility verified (no breaking changes)
- [x] Reviewer tags: @protocol-team @security-team

---

## Reviewer Notes

### Areas Requiring Special Attention
1. **Security Review**: Origin validation logic in `src/websocket/handshake.py:validate_origin()`
2. **Performance**: Frame masking/unmasking performance under load (see benchmarks)
3. **RFC Compliance**: Autobahn test results show full compliance, but manual review of edge cases welcome

### Testing Instructions for Reviewers
```bash
# 1. Run test suite
pytest tests/websocket/ -v --cov=src/websocket

# 2. Start local WebSocket server
python examples/websocket_server.py

# 3. Connect with wscat
wscat -c ws://localhost:8080/ws

# 4. Run Autobahn conformance suite (optional)
docker run -it --rm \
  -v "${PWD}/autobahn:/config" \
  crossbario/autobahn-testsuite \
  wstest -m fuzzingclient -s /config/fuzzingclient.json
```

---

## Related Work
- Feature Request: #245
- Real-time Notifications Epic: #189
- TLS Configuration: #312
- Future: WebSocket Multiplexing (RFC 8441): #401

---

**RFC 6455 Compliance**: ✅ Full Implementation  
**Autobahn Score**: 302/302 (100%)  
**Backward Compatibility**: ✅ No Breaking Changes
