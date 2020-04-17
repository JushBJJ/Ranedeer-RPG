import ptvsd
import RPG_main
#h ttps://code.visualstudio.com/docs/python/debugging#_attach-to-a-local-script

ip="127.0.0.1"
port=8080

ptvsd.enable_attach(address=(ip, port), redirect_output=True)

print(f"Attach Ready for ip {ip} at port {port}")

ptvsd.wait_for_attach()
RPG_main.main()