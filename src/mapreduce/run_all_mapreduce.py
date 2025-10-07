## #!/usr/bin/env python3
"""
Script để test MapReduce jobs locally (không cần Hadoop/HDFS)
Fixed: Module caching issue using subprocess
"""
import os
import sys
import subprocess
from pathlib import Path

def run_mapreduce_local(mapper_file, reducer_file, input_file, output_file):
    """
    Simulate MapReduce locally using subprocess (tránh cache module)
    """
    print(f"🚀 Running MapReduce locally...")
    print(f"   Mapper: {mapper_file}")
    print(f"   Reducer: {reducer_file}")
    print(f"   Input: {input_file}")
    print(f"   Output: {output_file}")
    
    try:
        # Step 1: Run Mapper
        print("\n📍 Step 1: Running Mapper...")
        with open(input_file, 'r', encoding='utf-8') as input_f:
            mapper_result = subprocess.run(
                ['python', mapper_file],
                stdin=input_f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
        
        if mapper_result.returncode != 0:
            print(f"❌ Mapper Error: {mapper_result.stderr}")
            return False
        
        mapper_output = mapper_result.stdout
        
        # Step 2: Sort (simulate shuffle & sort phase)
        print("📍 Step 2: Shuffle & Sort...")
        sorted_lines = sorted(mapper_output.strip().split('\n'))
        sorted_output = '\n'.join(sorted_lines)
        
        # Step 3: Run Reducer
        print("📍 Step 3: Running Reducer...")
        reducer_result = subprocess.run(
            ['python', reducer_file],
            input=sorted_output,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        if reducer_result.returncode != 0:
            print(f"❌ Reducer Error: {reducer_result.stderr}")
            return False
        
        reducer_output = reducer_result.stdout
        
        # Step 4: Write output
        print("📍 Step 4: Writing output...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(reducer_output)
        
        print(f"\n✅ Done! Output saved to: {output_file}")
        print("\n📊 Preview (first 10 lines):")
        lines = reducer_output.strip().split('\n')
        for i, line in enumerate(lines[:10]):
            print(f"   {line}")
        
        if len(lines) > 10:
            print(f"   ... ({len(lines) - 10} more lines)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test all jobs - TÊN THỰC TẾ CỦA THƯ MỤC
    jobs = [
        ("job01_brand_count", "Brand Count"),
        ("job02_word_count", "Word Count"),
        ("job03_price_range_analysis", "Price Range Analysis"),
        ("job04_ram_rom_distribution", "RAM/ROM Distribution"),
        ("job05_rating_by_brand", "Rating by Brand"),
        ("job06_discount_analysis", "Discount Analysis"),
        ("job07_cpu_analysis", "CPU Analysis"),
        ("job09_os_distribution", "OS Distribution"),
        ("job10_price_rating_correlation", "Price-Rating Correlation"),
        ("job08_discount_comparison_by_platform", "Discount Comparison by Platform"),
    ]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Sử dụng file đã có cột source_website
    input_file = os.path.join(base_dir, "../../data/raw/laptops_enriched_data_with_source.csv")
    output_base = os.path.join(base_dir, "../../output")
    
    # Create output directory
    os.makedirs(output_base, exist_ok=True)
    
    print("="*80)
    print("🧪 TESTING ALL MAPREDUCE JOBS LOCALLY")
    print("="*80)
    print(f"📁 Input: {input_file}")
    print(f"📁 Output: {output_base}")
    print()
    
    success_count = 0
    failed_jobs = []
    
    for job_dir, job_name in jobs:
        print(f"\n{'='*80}")
        print(f"📦 Testing: {job_name}")
        print('='*80)
        
        mapper_file = os.path.join(base_dir, job_dir, "mapper.py")
        reducer_file = os.path.join(base_dir, job_dir, "reducer.py")
        output_file = os.path.join(output_base, f"{job_dir}_local.txt")
        
        # Check if files exist
        if not os.path.exists(mapper_file):
            print(f"❌ Mapper not found: {mapper_file}\n")
            failed_jobs.append(job_name)
            continue
        
        if not os.path.exists(reducer_file):
            print(f"❌ Reducer not found: {reducer_file}\n")
            failed_jobs.append(job_name)
            continue
        
        # Create output directory if not exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        try:
            if run_mapreduce_local(mapper_file, reducer_file, input_file, output_file):
                success_count += 1
            else:
                failed_jobs.append(job_name)
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            failed_jobs.append(job_name)
        
        print()  # Empty line between jobs
    
    print(f"{'='*80}")
    print(f"📊 SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Success: {success_count}/{len(jobs)}")
    print(f"❌ Failed: {len(failed_jobs)}/{len(jobs)}")
    
    if failed_jobs:
        print(f"\n⚠️  Failed jobs:")
        for job in failed_jobs:
            print(f"   - {job}")
    else:
        print("\n🎉 ALL TESTS PASSED!")
    
    print(f"\n📁 Results saved in: {output_base}")
    print(f"{'='*80}")