import hashlib
import itertools
import threading
import time

ntlm_hash = "8846F7EAEE8FB117AD06BDD830B7586C"
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

event = threading.Event()

def guess_password(password):
   password = ''.join(password)
   ntlm_hash_guess = hashlib.new('md4', password.encode('utf-16le')).hexdigest()
   print(ntlm_hash_guess+":"+password)
   if ntlm_hash_guess == ntlm_hash.lower():
      print("The password is:", password)
      event.set()

start_time = time.time()
threads = []

for password in itertools.product(characters, repeat=8):
   thread = threading.Thread(target=guess_password, args=(password,))
   threads.append(thread)
   thread.start()
   if event.is_set():
      for thread in threads:
         thread.join()
      break

end_time = time.time()
elapsed_time = round(end_time - start_time)
print("Elapsed time:", elapsed_time)
