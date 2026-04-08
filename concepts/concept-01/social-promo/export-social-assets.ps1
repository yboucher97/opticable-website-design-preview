$ErrorActionPreference = "Stop"

$sourcePath = Join-Path $PSScriptRoot "spring-promo-social.html"
$sourceUri = [System.Uri]::new($sourcePath).AbsoluteUri
$outputDir = Join-Path $PSScriptRoot "..\\..\\..\\Images\\concepts\\concept-01\\generated-candidates\\spring-promo-2026-04"

New-Item -ItemType Directory -Force $outputDir | Out-Null

$exports = @(
  @{ Format = "square"; Name = "opticable-spring-promo-square-2160.png"; Size = "2160,2160" },
  @{ Format = "portrait"; Name = "opticable-spring-promo-portrait-2160x2700.png"; Size = "2160,2700" },
  @{ Format = "story"; Name = "opticable-spring-promo-story-2160x3840.png"; Size = "2160,3840" },
  @{ Format = "linkedin"; Name = "opticable-spring-promo-linkedin-2400x1254.png"; Size = "2400,1254" }
)

foreach ($export in $exports) {
  $targetPath = Join-Path $outputDir $export.Name
  $targetUrl = "$($sourceUri)?format=$($export.Format)"

  npx playwright screenshot $targetUrl $targetPath `
    --browser chromium `
    --viewport-size $export.Size `
    --wait-for-selector "body[data-ready='true']" `
    --wait-for-timeout 400 `
    --timeout 45000
}
