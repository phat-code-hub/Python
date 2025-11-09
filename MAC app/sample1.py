from Foundation import NSUserDefaults

# Get the standard user defaults
defaults = NSUserDefaults.standardUserDefaults()

# Set values
defaults.setObject_forKey_("Ueda", "username")
defaults.setInteger_forKey_(75, "volume")
defaults.synchronize()

# Retrieve values
print(defaults.stringForKey_("username"))
print(defaults.integerForKey_("volume"))




# import os
# import plistlib
# import Foundation
# import objc

# # Define the NSUserDefaults class
# NSUserDefaults = objc.lookUpClass('NSUserDefaults')

# # Save variables a and b using NSUserDefaults
# def save_to_nsuserdefaults(a, b):
#     defaults = NSUserDefaults.alloc().initWithSuiteName(None)
#     defaults.setValue(a, forKey:'a')
#     defaults.setValue(b, forKey:'b')
#     defaults.synchronize()

# # Load variables a and b from NSUserDefaults
# def load_from_nsuserdefaults():
#     defaults = NSUserDefaults.alloc().initWithSuiteName(None)
#     a = defaults.valueForKey_('a')
#     b = defaults.valueForKey_('b')
#     return a, b
# Save variables a and b into the "Documents" directory
# def save_to_docs(a, b):
#     docs_path = os.path.expanduser('~/Documents')
#     prefs_path = os.path.join(docs_path, 'prefs.plist')
#     with open(prefs_path, 'wb') as prefs_file:
#         # plist = plistlib.Plist()
#         plist = {}
#         plist['a'] = a
#         plist['b'] = b
#         plistlib.writePlist(plist, prefs_file)

# # Load variables a and b from the "Documents" directory
# def load_from_docs():
#     docs_path = os.path.expanduser('~/Documents')
#     prefs_path = os.path.join(docs_path, 'prefs.plist')
#     try:
#         with open(prefs_path, 'rb') as prefs_file:
#             plist = plistlib.load(prefs_file)
#             return plist.get('a'), plist.get('b')
#     except FileNotFoundError:
#         return None, None
    
# save_to_docs("English", "~/Documents/C_Shape/")

# Example usage
# a, b = load_from_docs()
# print(f"a: {a}, b: {b}")