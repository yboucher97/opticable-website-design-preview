"""Media and asset export helpers for the site generator."""

from sitegen_data import *

def deploy_asset_path_from_url(url):
    path = url.split('?', 1)[0]
    if not path.startswith('/'):
        return None
    return DEPLOY_ROOT / path.lstrip('/')


@lru_cache(maxsize=None)
def load_font(size, family='body'):
    candidates = FONT_CANDIDATES['display'] if family == 'display' else FONT_CANDIDATES['body']
    for font_path in candidates:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def text_width(draw, text, font):
    return draw.textbbox((0, 0), text, font=font)[2]


def ellipsize_text(draw, text, font, max_width):
    cleaned = ' '.join(text.split())
    if text_width(draw, cleaned, font) <= max_width:
        return cleaned
    words = cleaned.split()
    while words:
        candidate = ' '.join(words).rstrip(' ,.;:') + '…'
        if text_width(draw, candidate, font) <= max_width:
            return candidate
        words.pop()
    return '…'


def wrap_text_lines(draw, text, font, max_width, max_lines=None):
    words = text.split()
    if not words:
        return []
    lines = []
    current = words[0]
    for word in words[1:]:
        tentative = f'{current} {word}'
        if text_width(draw, tentative, font) <= max_width:
            current = tentative
        else:
            lines.append(current)
            current = word
    lines.append(current)
    if max_lines and len(lines) > max_lines:
        trailing = ' '.join(lines[max_lines - 1:])
        lines = lines[:max_lines - 1] + [ellipsize_text(draw, trailing, font, max_width)]
    return lines


def parse_image_position(position):
    parts = (position or 'center center').split()
    if len(parts) != 2:
        return (0.5, 0.5)

    def parse_part(value):
        value = value.strip().lower()
        named = {
            'left': 0.0,
            'center': 0.5,
            'right': 1.0,
            'top': 0.0,
            'bottom': 1.0,
        }
        if value in named:
            return named[value]
        if value.endswith('%'):
            try:
                return max(0.0, min(1.0, float(value[:-1]) / 100.0))
            except ValueError:
                return 0.5
        return 0.5

    return (parse_part(parts[0]), parse_part(parts[1]))


def blog_social_image_url(article_key, lang):
    return f'/assets/blog-social/{article_key}-{lang}.jpg?v={ASSET_VER}'


def blog_social_image_path(article_key, lang):
    return BLOG_SOCIAL_IMAGE_DIR / f'{article_key}-{lang}.jpg'


def export_blog_social_image(article_key, lang, article):
    target = blog_social_image_path(article_key, lang)
    source_path = deploy_asset_path_from_url(article.get('hero_image') or OG_IMAGE_URL)
    fallback_path = deploy_asset_path_from_url(OG_IMAGE_URL)
    if source_path is None or not source_path.exists():
        source_path = fallback_path
    if source_path is None or not source_path.exists():
        return

    try:
        with Image.open(source_path) as background:
            if (
                fallback_path
                and fallback_path.exists()
                and (background.width < BLOG_SOCIAL_IMAGE_WIDTH // 2 or background.height < BLOG_SOCIAL_IMAGE_HEIGHT // 2)
            ):
                with Image.open(fallback_path) as fallback:
                    background = fallback.convert('RGBA')
            else:
                background = background.convert('RGBA')
            canvas = ImageOps.fit(
                background,
                (BLOG_SOCIAL_IMAGE_WIDTH, BLOG_SOCIAL_IMAGE_HEIGHT),
                IMAGE_RESAMPLING.LANCZOS,
                centering=parse_image_position(article.get('hero_image_position', 'center center')),
            )
    except (FileNotFoundError, UnidentifiedImageError):
        if fallback_path is None or not fallback_path.exists():
            return
        with Image.open(fallback_path) as fallback:
            canvas = ImageOps.fit(
                fallback.convert('RGBA'),
                (BLOG_SOCIAL_IMAGE_WIDTH, BLOG_SOCIAL_IMAGE_HEIGHT),
                IMAGE_RESAMPLING.LANCZOS,
            )

    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(BLOG_SOCIAL_IMAGE_WIDTH):
        blend = x / max(1, BLOG_SOCIAL_IMAGE_WIDTH - 1)
        alpha = int(228 - (blend * 150))
        draw.line((x, 0, x, BLOG_SOCIAL_IMAGE_HEIGHT), fill=(7, 12, 10, max(0, alpha)))
    draw.rounded_rectangle((74, 60, 408, 112), radius=20, fill=(18, 45, 30, 216), outline=(122, 210, 150, 88), width=2)
    draw.rounded_rectangle((74, 134, 718, 566), radius=30, fill=(10, 18, 14, 116))

    eyebrow_font = load_font(26, 'body')
    headline_font = load_font(72, 'display')
    body_font = load_font(31, 'body')
    small_font = load_font(22, 'body')

    draw.text((100, 75), article.get('eyebrow', 'Opticable').upper(), font=eyebrow_font, fill=(198, 239, 214, 255))

    headline_lines = wrap_text_lines(draw, article['headline'], headline_font, 560, max_lines=4)
    y = 164
    for line in headline_lines:
        draw.text((96, y), line, font=headline_font, fill=(248, 252, 249, 255))
        y += 78

    max_excerpt_lines = max(0, min(3, (548 - (y + 14)) // 40))
    excerpt_lines = wrap_text_lines(draw, article.get('excerpt') or article.get('desc', ''), body_font, 560, max_lines=max_excerpt_lines)
    if excerpt_lines:
        y += 14
        for line in excerpt_lines:
            draw.text((98, y), line, font=body_font, fill=(214, 227, 218, 245))
            y += 40

    footer_text = 'Opticable Blog' if lang == 'en' else 'Blogue Opticable'
    if article.get('tags'):
        footer_text += '  |  ' + '  |  '.join(article['tags'][:2])
    draw.text((98, 584), footer_text, font=small_font, fill=(176, 214, 188, 255))

    image = Image.alpha_composite(canvas, overlay)
    target.parent.mkdir(parents=True, exist_ok=True)
    image.convert('RGB').save(target, format='JPEG', quality=80, optimize=True, progressive=True)
    IMAGE_DIMENSIONS_BY_URL[blog_social_image_url(article_key, lang)] = (BLOG_SOCIAL_IMAGE_WIDTH, BLOG_SOCIAL_IMAGE_HEIGHT)


def export_blog_social_images():
    for article_key, entry in BLOG_ARTICLES.items():
        for lang in ('en', 'fr'):
            localized = entry.get(lang)
            if not localized:
                continue
            export_blog_social_image(article_key, lang, localized)
    for article_key, entry in GUIDE_ARTICLE_DATA.items():
        for lang in ('en', 'fr'):
            localized = entry.get(lang)
            if not localized:
                continue
            export_blog_social_image(article_key, lang, localized)
    for article_key, entry in DECISION_ARTICLE_DATA.items():
        for lang in ('en', 'fr'):
            localized = entry.get(lang)
            if not localized:
                continue
            export_blog_social_image(article_key, lang, localized)


def export_image_variant(spec):
    source = spec['source']
    if not source.exists():
        return
    with Image.open(source) as image:
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        if spec.get('crop'):
            image = image.crop(spec['crop'])
        if spec.get('resize') and spec.get('canvas'):
            image = ImageOps.contain(image, spec['resize'], IMAGE_RESAMPLING.LANCZOS)
        elif spec.get('resize'):
            image.thumbnail(spec['resize'], IMAGE_RESAMPLING.LANCZOS)
        if spec.get('canvas'):
            background = spec.get('background', (255, 255, 255, 0))
            canvas = Image.new('RGBA', spec['canvas'], background)
            offset = ((canvas.width - image.width) // 2, (canvas.height - image.height) // 2)
            mask = image if 'A' in image.getbands() else None
            canvas.paste(image, offset, mask)
            image = canvas
        if spec['format'] == 'JPEG':
            if image.mode != 'RGB':
                image = image.convert('RGB')
            save_kwargs = {'format': 'JPEG', 'quality': spec['quality'], 'optimize': True, 'progressive': True}
        elif spec['format'] == 'PNG':
            png_colors = spec.get('png_colors')
            if png_colors:
                image = image.quantize(colors=png_colors)
            save_kwargs = {'format': 'PNG', 'optimize': True}
        elif spec['format'] == 'AVIF':
            if image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGBA')
            save_kwargs = {'format': 'AVIF', 'quality': spec['quality'], 'speed': 6}
        else:
            save_kwargs = {'format': 'WEBP', 'quality': spec['quality'], 'method': 6}
        spec['target'].parent.mkdir(parents=True, exist_ok=True)
        image.save(spec['target'], **save_kwargs)


def export_home_images():
    for spec in HOME_IMAGE_EXPORTS:
        export_image_variant(spec)


def reset_deploy_dir():
    shutil.rmtree(DEPLOY_ROOT, ignore_errors=True)
    DEPLOY_ASSET_ROOT.mkdir(parents=True, exist_ok=True)


def copy_static_assets():
    for name in STATIC_ASSET_FILES:
        source = SOURCE_ASSET_ROOT / name
        if not source.exists():
            continue
        shutil.copy2(source, DEPLOY_ASSET_ROOT / name)
    for spec in RUNTIME_ASSET_COPIES:
        source = spec['source']
        if not source.exists():
            continue
        shutil.copy2(source, spec['target'])


def remove_legacy_root_build():
    for name in LEGACY_ROOT_BUILD_DIRS:
        shutil.rmtree(root / name, ignore_errors=True)
    for name in LEGACY_ROOT_BUILD_FILES:
        path = root / name
        if path.exists():
            path.unlink()
    for name in ROOT_GENERATED_ASSET_FILES:
        path = SOURCE_ASSET_ROOT / name
        if path.exists():
            path.unlink()


