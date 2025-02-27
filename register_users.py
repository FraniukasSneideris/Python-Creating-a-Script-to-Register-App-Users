import argparse

class Validate:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def validate_name(self):
      if type(self.name) != str:
        return False

      elif len(self.name) <= 2:
        return False

      else:
        return True


    def validate_email(self):
      top_level_domains = [".org", ".net", ".edu", ".ac", ".uk", ".com"]
      valid_email = False
      username = self.email.split('@')[0]

      if '@' not in self.email:
        return valid_email

      if len(username) < 1:
        return valid_email

      for domain in top_level_domains:
        if domain in self.email:
            valid_email = True

      return valid_email

    def validate_password(self):
      has_capital = False
      has_number = False

      if len(self.password) < 8:
        return False

      for char in self.password:
        if "A" <= char <= "Z":
           has_capital = True
        if "0" <= char <= "9":
           has_number = True

      if has_capital and has_number:
          return True
      else:
          return False



class RegisterUser(Validate):

  def __init__(self, name, email, password):
     Validate.__init__(self, name, email, password)

  def validate_user(self):
    if not Validate.validate_name(self):
      raise ValueError("Name validation failed.")

    elif not Validate.validate_email(self):
        raise ValueError("Email validation failed.")

    elif not Validate.validate_password(self):
        raise ValueError("Password validation failed.")

    return True

  def register_user(self):
    user = {}
    try:
       self.validate_user()
    except:
        return False

    user['name'] = self.name
    user['email'] = self.email
    user['password'] = self.password

    return user


class Bulk:

  def __init__(self, file):
    self.file = file
    self.bulk_file = None
    self.processed_data = []
    self.new_users = []

  def open_user_data(self):
    with open(self.file, 'r') as f:
      self.bulk_file = f.readlines()
  
  def process_user_data(self):
    is_header = True
    
    for line in self.bulk_file:
        if is_header:
            is_header = False  
            continue     
        self.processed_data.append(line.strip().split(','))
        
    return self.processed_data

  def register_bulk(self):
     for single_user in self.processed_data:
      user = RegisterUser(single_user[0], single_user[1], single_user[2])
      if user.validate_user():
         self.new_users.append({
            'name': single_user[0],
            'email': single_user[1],
            'password': single_user[2]
            })

     return self.new_users


def main():
  parser = argparse.ArgumentParser(description="Registers and validates new users individually or as a multiple registration (bulk).")
  parser.add_argument("name", type=str, nargs="?", help="Name of the new user entered with quotes.")
  parser.add_argument("email", type=str, nargs="?", help="Email of the new user entered with quotes.")
  parser.add_argument("password", type=str, nargs="?", help="Password of the new user entered with quotes.")
  parser.add_argument("action", choices=['validate', 'register'], nargs="?", help="Choose either validate or register, depnding on the wanted action.")
  parser.add_argument("--bulk", action="store_true", help="Use only for bulk registration.")
  parser.add_argument("--file", type=str, nargs="?", help="Use only for bulk registration.")
  args = parser.parse_args()

  if args.action == 'validate':
    try:
       RegisterUser(args.name, args.email, args.password).validate_user()
       print("Validation successful!")
    except ValueError as e:
       print(f"Validation failed: {e}")
  
  elif args.action == 'register':
    print(RegisterUser(args.name, args.email, args.password).register_user())
  
  elif args.bulk:
    if args.file:
       bulk_file_raw = Bulk(args.file)
       bulk_file_raw.open_user_data()
       bulk_file_raw.process_user_data()
       print(bulk_file_raw.register_bulk())
    else:
       print("Error: A file should be added to use --bulk.")
     
if __name__ == "__main__":
  main()