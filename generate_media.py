"""
generate_media.py

Scans your local media folders and writes out the SONGS / ARTWORKS
array text, ready to paste into portfolio.html.

FOLDER STRUCTURE THIS EXPECTS (create these next to this script):

  videos/     -> your song snippet .mp4 files
  covers/     -> thumbnail images for each song, SAME base filename
                 as the matching video (e.g. slow-fire.mp4 pairs with
                 covers/slow-fire.jpg)
  artworks/   -> your artwork image files (.jpg, .png, etc.)

USAGE:
  1. Put this script in the same folder as your videos/, covers/,
     and artworks/ folders.
  2. Run it:  python3 generate_media.py
  3. It creates generated-media.js with the SONGS and ARTWORKS arrays.
  4. Open generated-media.js, copy its contents, and paste them over
     the existing SONGS / ARTWORKS block in portfolio.html.
  5. Titles are guessed from the filename (dashes/underscores become
     spaces, capitalized). The "sub" field (year/caption) is left as
     a placeholder "20XX" for you to edit by hand afterward.

Nothing here uploads or sends your files anywhere — it only reads
filenames on your own computer and writes a text file next to it.
"""

import os

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
VIDEO_EXTS = {'.mp4', '.mov', '.webm'}

VIDEOS_DIR = 'videos'
COVERS_DIR = 'covers'
ARTWORKS_DIR = 'artworks'
OUTPUT_FILE = 'generated-media.js'


def title_from_filename(filename):
    name = os.path.splitext(filename)[0]
    name = name.replace('-', ' ').replace('_', ' ').strip()
    return name.title() if name else 'Untitled'


def find_cover_for(base_name):
    """Look in covers/ for a file matching base_name with any known image extension."""
    if not os.path.isdir(COVERS_DIR):
        return None
    for ext in IMAGE_EXTS:
        candidate = os.path.join(COVERS_DIR, base_name + ext)
        if os.path.isfile(candidate):
            return candidate.replace('\\', '/')
    return None


def list_media(folder, exts):
    if not os.path.isdir(folder):
        return []
    files = sorted(os.listdir(folder))
    return [f for f in files if os.path.splitext(f)[1].lower() in exts and not f.startswith('.')]


def build_songs():
    videos = list_media(VIDEOS_DIR, VIDEO_EXTS)
    lines = []
    missing_covers = []
    for v in videos:
        base = os.path.splitext(v)[0]
        video_path = f'{VIDEOS_DIR}/{v}'
        cover_path = find_cover_for(base)
        if cover_path is None:
            missing_covers.append(v)
            cover_path = 'images/PLACEHOLDER.jpg'
        title = title_from_filename(v)
        lines.append(
            f"  {{cover:'{cover_path}', video:'{video_path}', title:'{title}', sub:'20XX'}},"
        )
    return lines, missing_covers


def build_artworks():
    images = list_media(ARTWORKS_DIR, IMAGE_EXTS)
    lines = []
    for img in images:
        title = title_from_filename(img)
        lines.append(
            f"  {{img:'{ARTWORKS_DIR}/{img}', title:'{title}', sub:'Medium — 20XX'}},"
        )
    return lines


def main():
    song_lines, missing_covers = build_songs()
    artwork_lines = build_artworks()

    out = []
    out.append('const SONGS = [')
    out.extend(song_lines if song_lines else ["  // no files found in videos/"])
    out.append('];')
    out.append('')
    out.append('const ARTWORKS = [')
    out.extend(artwork_lines if artwork_lines else ["  // no files found in artworks/"])
    out.append('];')

    with open(OUTPUT_FILE, 'w') as f:
        f.write('\n'.join(out) + '\n')

    print(f'Found {len(song_lines)} song(s) and {len(artwork_lines)} artwork(s).')
    print(f'Written to {OUTPUT_FILE} — open it, copy the contents, and paste')
    print('them over the SONGS / ARTWORKS block in portfolio.html.')
    if missing_covers:
        print('')
        print('NOTE: no matching cover image found in covers/ for:')
        for m in missing_covers:
            print(f'  - {m}')
        print('These were given a placeholder cover path — add a matching')
        print('image to covers/ (same filename) and re-run, or edit by hand.')


if __name__ == '__main__':
    main()