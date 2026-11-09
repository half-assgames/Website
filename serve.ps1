# Previews the website on this PC, the way GitHub Pages will serve it.
# Easiest: double-click preview.cmd. Or run:  .\serve.ps1 -Open
# Then visit http://localhost:8080/ . Press Ctrl+C (or close the window) to stop.

param(
    [int]$Port = 8080,
    [string]$Root = (Join-Path $PSScriptRoot 'docs'),
    [switch]$Open
)

$types = @{
    '.html'  = 'text/html; charset=utf-8'
    '.css'   = 'text/css; charset=utf-8'
    '.js'    = 'text/javascript; charset=utf-8'
    '.json'  = 'application/json'
    '.xml'   = 'application/xml'
    '.txt'   = 'text/plain; charset=utf-8'
    '.svg'   = 'image/svg+xml'
    '.png'   = 'image/png'
    '.jpg'   = 'image/jpeg'
    '.webp'  = 'image/webp'
    '.ico'   = 'image/x-icon'
    '.woff2' = 'font/woff2'
}

$rootFull = [IO.Path]::GetFullPath($Root).TrimEnd('\') + '\'
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()
Write-Host "Previewing $rootFull"
Write-Host "Open http://localhost:$Port/ in your browser. Ctrl+C stops it."
if ($Open) { Start-Process "http://localhost:$Port/" }

try {
    while ($listener.IsListening) {
        $task = $listener.GetContextAsync()
        while (-not $task.AsyncWaitHandle.WaitOne(250)) { }   # keeps Ctrl+C working
        $ctx = $task.GetAwaiter().GetResult()
        $res = $ctx.Response
        try {
            $urlPath = [Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath)
            $file = [IO.Path]::GetFullPath((Join-Path $rootFull $urlPath.TrimStart('/')))
            $status = 200

            if (-not $file.StartsWith($rootFull, [StringComparison]::OrdinalIgnoreCase) -and ($file + '\') -ne $rootFull) {
                $file = $null
            }
            elseif (Test-Path -LiteralPath $file -PathType Container) {
                if (-not $urlPath.EndsWith('/')) {
                    # GitHub Pages adds the trailing slash to folder addresses too
                    $res.StatusCode = 301
                    $res.RedirectLocation = $urlPath + '/'
                    $res.Close()
                    Write-Host "301 $urlPath"
                    continue
                }
                $file = Join-Path $file 'index.html'
            }

            if (-not $file -or -not (Test-Path -LiteralPath $file -PathType Leaf)) {
                $status = 404
                $file = Join-Path $rootFull '404.html'
            }

            $bytes = [IO.File]::ReadAllBytes($file)
            $ext = [IO.Path]::GetExtension($file).ToLowerInvariant()
            $res.StatusCode = $status
            $res.ContentType = if ($types.ContainsKey($ext)) { $types[$ext] } else { 'application/octet-stream' }
            $res.Headers['Cache-Control'] = 'no-store'
            $res.ContentLength64 = $bytes.Length
            $res.OutputStream.Write($bytes, 0, $bytes.Length)
            Write-Host "$status $urlPath"
        }
        catch {
            Write-Host "500 $($_.Exception.Message)"
            try { $res.StatusCode = 500 } catch { }
        }
        finally {
            $res.Close()
        }
    }
}
finally {
    $listener.Stop()
}
