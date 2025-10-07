#!/usr/bin/env python3
"""
Web Scraper cho Thế Giới Di Động (thegioididong.com)
Thu thập thông tin laptop
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

def scrape_tgdd():
    """
    Cào dữ liệu laptop từ thegioididong.com
    """
    base_url = "https://www.thegioididong.com/laptop"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    products = []
    
    print("Bắt đầu cào dữ liệu laptop từ Thế Giới Di Động...")
    
    # TODO: Implement scraping logic
    # 1. Lấy danh sách các trang sản phẩm laptop
    # 2. Với mỗi trang, lấy danh sách sản phẩm
    # 3. Với mỗi sản phẩm, lấy chi tiết:
    #    - id, product_name, current_price, list_price
    #    - brand, category, cpu, ram, storage
    #    - screen_size, screen_resolution, os, software
    #    - average_rating, product_url
    # 4. Lưu vào list products
    
    # Ví dụ dữ liệu mẫu:
    # products.append({
    #     'id': 1,
    #     'product_name': 'Laptop HP 15 fc0085AU',
    #     'current_price': 13190000,
    #     'list_price': 14890000,
    #     'brand': 'HP',
    #     'category': 'Laptop',
    #     'cpu': 'R5 7430U',
    #     'ram': '16GB',
    #     'storage': '512GB',
    #     'screen_size': '15.6 inch',
    #     'screen_resolution': 'Full HD',
    #     'os': 'Windows 11',
    #     'software': 'N/A',
    #     'average_rating': 4.9,
    #     'product_url': 'https://...'
    # })
    
    return products

def save_to_csv(products, filename="../../data/raw/laptops_tgdd.csv"):
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
    products = scrape_tgdd()
    save_to_csv(products)
