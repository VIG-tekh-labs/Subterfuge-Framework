# Subterfuge Web dashboard — local and remote server access

Subterfuge can be installed on a computer with a graphical desktop or on a
headless Linux server. It does not require the native Qt GUI to offer its
Web dashboard. The Qt interface and Web interface use the same Python core,
but remain separate launch modes.

## Localhost access — default, safest setup

On a computer or on the server:

    subterfuge serve --port 8080

Open this address in a browser on **the same machine**:

    http://127.0.0.1:8080/

Use a different available port if 8080 is busy:

    subterfuge serve --port 9080

    http://127.0.0.1:9080/

The Web server binds exclusively to 127.0.0.1. It does not silently
listen on 0.0.0.0, on a public IP, or on all network interfaces.

## Secure remote access using the server IP address and SSH port

Suppose your server is reachable at 192.0.2.10 via SSH port 22.
Start the Web interface *on the server*:

    subterfuge serve --port 8080

On your personal computer, start a secure SSH tunnel to that server:

    ssh -N -L 127.0.0.1:8080:127.0.0.1:8080 -p 22 username@192.0.2.10

Then open on your personal computer:

    http://127.0.0.1:8080/

The SSH connection uses the actual server IP address and port. The browser
address is localhost because SSH securely forwards the local port to the
server's loopback dashboard. There is no unauthenticated public HTTP server.
You can specify a different local port:

    ssh -N -L 127.0.0.1:9080:127.0.0.1:8080 -p 2222 username@192.0.2.10

    http://127.0.0.1:9080/

With an appropriate SSH client and port forwarding, a mobile browser can
also access a remotely hosted Subterfuge dashboard through a tunnel. A
native mobile application is not yet implemented.

## Optional direct HTTPS URL using a trusted reverse proxy

For a public or private server at a fixed IP, a separate HTTPS reverse
proxy with authentication can expose Subterfuge as, for example:

    https://192.0.2.10:8443/

The HTTPS certificate must be valid and trusted for that IP (or for a
corresponding DNS hostname). The proxy MUST require authenticated users,
forward requests to the locally bound Python dashboard, rewrite its
upstream Host header to 127.0.0.1:8080, preserve the original Origin header,
and enforce HTTPS. Do not publish port 8080 directly.

Explicitly declare the HTTPS origin expected by the browser:

    subterfuge serve --port 8080 --public-origin https://192.0.2.10:8443

The internal dashboard **still binds only to 127.0.0.1:8080**.
The optional public-origin argument adds exactly one trusted HTTPS browser
origin to the existing Host / Origin / per-session token checks; it does
not itself activate networking, TLS certificates or authentication.

A representative Caddy 2 reverse-proxy configuration, for a properly
managed, trusted HTTPS certificate and pre-created password hash:

    https://192.0.2.10:8443 {
        tls /etc/subterfuge/tls/fullchain.pem /etc/subterfuge/tls/privkey.pem
        basic_auth {
            analyst $2a$14$REPLACE_WITH_REAL_BCRYPT_HASH
        }
        reverse_proxy 127.0.0.1:8080 {
            header_up Host 127.0.0.1:8080
        }
    }

The example is a template, **not a ready-to-deploy password**. Use the
reverse proxy's documented password-hashing utility and private file
permissions, install a trusted certificate, restrict firewall access,
and verify the authentication policy before exposing a production system.
Caddy and its configuration are NOT installed automatically by Subterfuge.
Any reverse proxy equivalent to this deployment pattern may be used.

If the public server uses a DNS hostname instead of an IP address, specify
that exact HTTPS origin, including its visible port, in --public-origin.
For example:

    subterfuge serve --port 8080 --public-origin https://audit.example.net:8443

    https://audit.example.net:8443/

The localhost dashboard and SSH tunnel modes require **no** public-origin
flag and keep the original same-origin restrictions.

## Native GUI on PCs

On a computer with a graphical desktop, install the optional desktop extra:

    python -m pip install ".[desktop]"
    subterfuge gui

This opens an actual Qt application, without a browser or server. The
application may also be launched with subterfuge-desktop; Linux users can
create an application-menu shortcut with subterfuge desktop-shortcut.
Use the Web mode on a headless server, or whenever a browser is preferred.

The two interfaces do not automatically synchronize reports or scan state.
They share the analysis code, and reports can be exchanged with JSON
files. Future authenticated multi-user and mobile features require separate
design and testing.
