from app import *
from app.etl.controllers import *
from app.gui.ui_compiler import UICompiler


if __name__ == "__main__":
    app = UICompiler()
    app.mainloop()
