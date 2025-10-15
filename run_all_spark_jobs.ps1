# Script chạy tất cả các Spark jobs
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Bắt đầu chạy tất cả Spark jobs" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$jobs = @(
    "job01_avg_price_by_brand.py",
    "job02_discount_rate_by_brand.py",
    "job03_price_range_distribution.py",
    "job05_top5_highest_discounts.py",
    "job07_popular_cpu_models.py",
    "job08_product_count_by_brand_store.py",
    "job09_top5_rated_products.py",
    "job10_ram_storage_distribution.py",
    "job11_top5_screen_specs.py"
)

$completed = 0
$failed = 0

foreach ($job in $jobs) {
    Write-Host "`n----------------------------------------" -ForegroundColor Yellow
    Write-Host "Đang chạy: $job" -ForegroundColor Yellow
    Write-Host "----------------------------------------" -ForegroundColor Yellow
    
    spark-submit "src/spark/$job"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $job thành công!" -ForegroundColor Green
        $completed++
    } else {
        Write-Host "❌ $job thất bại!" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Kết quả chạy Spark jobs:" -ForegroundColor Cyan
Write-Host "  Thành công: $completed/$($jobs.Count)" -ForegroundColor Green
Write-Host "  Thất bại: $failed/$($jobs.Count)" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan
