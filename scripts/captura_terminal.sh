#!/bin/bash
# Captura REAL de una ventana de Terminal.app ejecutando un comando.
# Uso: captura_terminal.sh <directorio> <salida.png> <columnas> <filas> <comando...>
# El comando se muestra literal (desde un archivo temporal) y luego se ejecuta en la misma ventana;
# se espera a que termine, se captura solo esa ventana (screencapture -l) y se cierra.
set -euo pipefail
DIR="$1"; OUT="$2"; COLS="$3"; ROWS="$4"; shift 4
CMD="$*"
TMPD=$(mktemp -d /tmp/captura-term.XXXXXX)
printf '%s\n' "$CMD" > "$TMPD/cmd.txt"
cat > "$TMPD/run.sh" <<RUN
cd "$DIR" || exit 1
clear
printf '%s %% ' "\$(basename "\$PWD")"; cat "$TMPD/cmd.txt"
bash "$TMPD/cmd.txt"
RUN
WID=$(osascript <<OSA
tell application "Terminal"
  set t to do script ""
  delay 1.2
  set w to first window whose tabs contains t
  set number of columns of w to $COLS
  set number of rows of w to $ROWS
  delay 0.8
  do script "clear; bash $TMPD/run.sh" in t
  delay 1
  repeat 900 times
    if busy of t is false then exit repeat
    delay 0.5
  end repeat
  delay 1
  return (id of w as text) & " " & (number of columns of w as text) & "x" & (number of rows of w as text)
end tell
OSA
)
ID=${WID%% *}
screencapture -x -o -l "$ID" "$OUT"
osascript -e "tell application \"Terminal\" to close window id $ID" >/dev/null 2>&1 || true
rm -rf "$TMPD"
echo "$OUT (ventana $WID)"
