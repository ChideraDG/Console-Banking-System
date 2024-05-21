"""
1. **Text Formatting:**
   - `\033[0m`: Reset all text formatting to default.
   - `\033[1m`: Bold text.
   - `\033[2m`: Dim text (rarely supported).
   - `\033[3m`: Italic text (not widely supported).
   - `\033[4m`: Underlined text.
   - `\033[7m`: Inverted colors (swap foreground and background colors).
   - `\033[8m`: Hidden text (invisible).
"""


end = '\033[0m'


bold = '\033[1m'


dim = '\033[2m'


italic = '\033[3m'


underline = '\033[4m'


inverted_colors = '\033[7m'


hidden = '\033[8m'


"""
2. **Text Colors:**
   - `\033[30m`: Black text.
   - `\033[31m`: Red text.
   - `\033[32m`: Green text.
   - `\033[33m`: Yellow text.
   - `\033[34m`: Blue text.
   - `\033[35m`: Magenta text.
   - `\033[36m`: Cyan text.
   - `\033[37m`: White text.
   - `\033[90m`: Bright black (gray) text.
   - `\033[91m`: Bright red text.
   - `\033[92m`: Bright green text.
   - `\033[93m`: Bright yellow text.
   - `\033[94m`: Bright blue text.
   - `\033[95m`: Bright magenta text.
   - `\033[96m`: Bright cyan text.
   - `\033[97m`: Bright white text.
"""


black = '\033[30m'


red = '\033[31m'


green = '\033[32m'


yellow = '\033[33m'


blue = '\033[34m'


magenta = '\033[35m'


cyan = '\033[36m'


white = '\033[37m'


brt_black = '\033[90m'


brt_red = '\033[91m'


brt_green = '\033[92m'


brt_yellow = '\033[93m'


brt_blue = '\033[94m'


brt_magenta = '\033[95m'


brt_cyan = '\033[96m'


brt_white = '\033[97m'


"""
3. **Background Colors:**
   - `\033[40m`: Black background.
   - `\033[41m`: Red background.
   - `\033[42m`: Green background.
   - `\033[43m`: Yellow background.
   - `\033[44m`: Blue background.
   - `\033[45m`: Magenta background.
   - `\033[46m`: Cyan background.
   - `\033[47m`: White background.
   - `\033[100m`: Bright black (gray) background.
   - `\033[101m`: Bright red background.
   - `\033[102m`: Bright green background.
   - `\033[103m`: Bright yellow background.
   - `\033[104m`: Bright blue background.
   - `\033[105m`: Bright magenta background.
   - `\033[106m`: Bright cyan background.
   - `\033[107m`: Bright white background.
"""


black_bg = '\033[40m'


red_bg = '\033[41m'


green_bg = '\033[42m'


yellow_bg = '\033[43m'


blue_bg = '\033[44m'


magenta_bg = '\033[45m'


cyan_bg = '\033[46m'


white_bg = '\033[47m'


brt_black_bg = '\033[100m'


brt_red_bg = '\033[101m'


brt_green_bg = '\033[102m'


brt_yellow_bg = '\033[103m'


brt_blue_bg = '\033[104m'


brt_magenta_bg = '\033[105m'


brt_cyan_bg = '\033[106m'


brt_white_bg = '\033[107m'


