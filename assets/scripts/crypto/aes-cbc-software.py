import wx
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

KEY_SIZE = 16  
BLOCK_SIZE = AES.block_size 


def generate_key_and_iv():
    key = get_random_bytes(KEY_SIZE)
    iv = get_random_bytes(BLOCK_SIZE)
    return key, iv


def save_key(key, iv, key_file_path):
    with open(key_file_path, 'wb') as f:
        f.write(key + iv)


def load_key(key_file_path):
    with open(key_file_path, 'rb') as f:
        data = f.read()
        key = data[:KEY_SIZE]
        iv = data[KEY_SIZE:KEY_SIZE + BLOCK_SIZE]
        return key, iv


def encrypt_file(input_file_path, output_file_path, key_file_path):
    key, iv = generate_key_and_iv()
    save_key(key, iv, key_file_path)

    with open(input_file_path, 'rb') as f:
        plaintext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, BLOCK_SIZE))

    with open(output_file_path, 'wb') as f:
        f.write(ciphertext)


def decrypt_file(input_file_path, output_file_path, key_file_path):
    key, iv = load_key(key_file_path)

    with open(input_file_path, 'rb') as f:
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)

    with open(output_file_path, 'wb') as f:
        f.write(plaintext)


def read_file_hex(path):
    try:
        with open(path, 'rb') as f:
            return f.read().hex()
    except Exception:
        return ""


class CryptoFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="AES-CBC Encrypt/Decrypt", size=(700, 400))
        panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(rows=3, cols=3, vgap=5, hgap=5)

        self.input_txt = wx.TextCtrl(panel)
        self.output_txt = wx.TextCtrl(panel)
        self.key_txt = wx.TextCtrl(panel)

        grid.AddMany([
            (wx.StaticText(panel, label="Name of input file:")), (self.input_txt, 1, wx.EXPAND), (wx.Button(panel, label="Encrypt"), 0, wx.ALIGN_CENTER),
            (wx.StaticText(panel, label="Name of output file:")), (self.output_txt, 1, wx.EXPAND), (wx.Button(panel, label="Decrypt"), 0, wx.ALIGN_CENTER),
            (wx.StaticText(panel, label="Name of key file:")), (self.key_txt, 1, wx.EXPAND), (wx.StaticText(panel)),  # empty
        ])
        grid.AddGrowableCol(1, 1)
        main_sizer.Add(grid, 0, wx.ALL | wx.EXPAND, 10)

        text_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.input_hex = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.output_hex = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        text_sizer.Add(self.input_hex, 1, wx.ALL | wx.EXPAND, 5)
        text_sizer.Add(self.output_hex, 1, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(text_sizer, 1, wx.EXPAND)

        panel.SetSizer(main_sizer)

        # Events
        self.Bind(wx.EVT_BUTTON, self.on_encrypt, grid.GetItem(2).GetWindow())
        self.Bind(wx.EVT_BUTTON, self.on_decrypt, grid.GetItem(5).GetWindow())

    def on_encrypt(self, event):
        input_file = self.input_txt.GetValue()
        output_file = self.output_txt.GetValue()
        key_file = self.key_txt.GetValue()

        try:
            encrypt_file(input_file, output_file, key_file)
            self.input_hex.SetValue(read_file_hex(input_file))
            self.output_hex.SetValue(read_file_hex(output_file))
        except Exception as e:
            wx.MessageBox(f"Encryption error: {str(e)}", "Error", wx.ICON_ERROR)

    def on_decrypt(self, event):
        input_file = self.input_txt.GetValue()
        output_file = self.output_txt.GetValue()
        key_file = self.key_txt.GetValue()

        try:
            decrypt_file(input_file, output_file, key_file)
            self.input_hex.SetValue(read_file_hex(input_file))
            self.output_hex.SetValue(read_file_hex(output_file))
        except Exception as e:
            wx.MessageBox(f"Decryption error: {str(e)}", "Error", wx.ICON_ERROR)


if __name__ == "__main__":
    app = wx.App(False)
    frame = CryptoFrame()
    frame.Show()
    app.MainLoop()