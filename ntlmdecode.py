import hashlib
import itertools
import math
import threading
import time

ntlm_hash = "0CB6948805F797BF2A82807973B89537"
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
knownchars = ""

event = threading.Event()

def guess_password(password):
   password = ''.join(password)
   password = knownchars+password
   ntlm_hash_guess = hashlib.new('md4', password.encode('utf-16le')).hexdigest()
   print(ntlm_hash_guess+":"+password)
   if ntlm_hash_guess == ntlm_hash.lower():
      print("The password is:", password)
      event.set()

start_time = time.time()

threads = []

for length in range(1,13):
   for password in itertools.product(characters, repeat=length):
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
