from Foundation import NSUserDefaults

app_id = "com.mycompany.myapp"
a, b = 123, "Hello"

# Get defaults for this app
defaults = NSUserDefaults.alloc().initWithSuiteName_(app_id)

# Save
defaults.setObject_forKey_(a, "a")
defaults.setObject_forKey_(b, "b")
defaults.synchronize()

# Read back
a_val = defaults.objectForKey_("a")
b_val = defaults.objectForKey_("b")

print(a_val, b_val)
