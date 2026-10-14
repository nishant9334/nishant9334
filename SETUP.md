# Animated GitHub profile README - setup (Windows-friendly)

Your GitHub username is nishant9334, so these commands are ready to paste.

## 1. Create the magic repo
Create a PUBLIC repo named exactly nishant9334 (github.com/new) - you currently have only b100-intelligence, Fresh-mart and ResumeIQ, so this one is new, tick "Add a README", then:

    git clone https://github.com/nishant9334/nishant9334.git
    cd nishant9334

Copy everything from this kit (scripts/, data/, .github/, README.md) into that folder.
(.github is a hidden folder - make sure it gets copied too.)

## 2. Python toolchain
    python -m venv .venv
    .venv\Scripts\activate          (Mac/Linux: source .venv/bin/activate)
    pip install -r scripts/requirements.txt

If rembg / opencv-python are slow or fail to install, install only the light set first:
    pip install requests beautifulsoup4 pillow numpy

## 3. Portrait (optional but it's the signature look)
Use a clear, front-facing photo with good light. Then:

    python scripts/prep_photo.py my-photo.jpg
    python scripts/make_ascii_svg.py

## 4. Info card
Edit the ROWS list at the top of scripts/make_info_card.py, then:

    python scripts/make_info_card.py

## 5. Heatmap
    set GITHUB_USER=nishant9334           (cmd)
    $env:GITHUB_USER="nishant9334"        (PowerShell)
    python scripts/fetch_contributions.py
    python scripts/render_heatmap_svg.py

## 6. Push
    git add .
    git commit -m "feat: animated profile README"
    git push

## 7. Turn on the daily refresh
Repo -> Settings -> Actions -> General -> Workflow permissions -> "Read and write permissions" -> Save.
Then Actions tab -> "Update profile art" -> Run workflow, and check it commits a fresh contrib-heatmap.svg.

Tip: SVG animations only play when the image is loaded directly on github.com/nishant9334,
not in some local markdown previews. Hard-refresh (Ctrl+Shift+R) to replay them.
