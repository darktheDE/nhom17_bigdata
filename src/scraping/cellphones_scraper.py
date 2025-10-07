#!/usr/bin/env python3
"""
Web Scraper cho CellphoneS (cellphones.com.vn)
Thu thập thông tin laptop
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

def scrape_cellphones():
    """
    Cào dữ liệu laptop từ cellphones.com.vn
    """
    base_url = "https://cellphones.com.vn/laptop.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    products = []
    
    print("Bắt đầu cào dữ liệu laptop từ CellphoneS...")
    
    # TODO: Implement scraping logic
    # 1. Lấy danh sách các trang sản phẩm laptop
    # 2. Với mỗi trang, lấy danh sách sản phẩm
    # 3. Với mỗi sản phẩm, lấy chi tiết:
    #    - id, product_name, current_price, list_price
    #    - brand, category, cpu, ram, storage
    #    - screen_size, screen_resolution, os, software
    #    - average_rating, product_url
    # 4. Lưu vào list products
    
    return products

def save_to_csv(products, filename="../../data/raw/laptops_cellphones.csv"):
    """
    Lưu dữ liệu vào file CSV
    """
    if not products:
        print("Không có dữ liệu để lưu")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
    
    print(f"Đã lưu {len(products)} sản phẩm vào {filename}")

if __name__ == "__main__":
    products = scrape_cellphones()
    save_to_csv(products)
