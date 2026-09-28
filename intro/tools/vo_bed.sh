#!/bin/sh
# Voiceover bed for the MyChart explainer: EQ the music stem (a dip where speech lives), sum it with the foley stem,
# and set one fixed gain so the mix sits at -23 LUFS (stems get the same gain, so they still add up to the mix).
set -e
O=out/rossen-mychart-scam
ffmpeg -v error -y -i $O/score_music.wav -af "equalizer=f=2200:t=q:w=1.1:g=-5,equalizer=f=450:t=q:w=1:g=-2.5" $O/_music_eq.wav
ffmpeg -v error -y -i $O/_music_eq.wav -i $O/score_sfx.wav -filter_complex "amix=inputs=2:normalize=0" $O/_mix.wav
LU=$(ffmpeg -v info -i $O/_mix.wav -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(-23 - ($LU))")
for s in music_eq:bed_music mix:bed_mix; do in=${s%%:*}; outn=${s##*:}; ffmpeg -v error -y -i $O/_$in.wav -af "volume=${G}dB,alimiter=limit=0.84:level=false" $O/$outn.wav; done
ffmpeg -v error -y -i $O/score_sfx.wav -af "volume=${G}dB" $O/bed_sfx.wav
rm $O/_music_eq.wav $O/_mix.wav
echo "mix was $LU LUFS, gain $G dB"
