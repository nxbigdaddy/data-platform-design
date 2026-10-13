import time
import requests
import concurrent.futures

BASE_URL = "http://localhost:8000"

# 测试响应时间
def test_response_time():
    """测试API响应时间"""
    endpoints = [
        "/health",
        "/api/datasource",
        "/api/sync/task",
        "/api/service/monitor"
    ]
    
    response_times = []
    
    for endpoint in endpoints:
        url = f"{BASE_URL}{endpoint}"
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        response_time = end_time - start_time
        response_times.append((endpoint, response_time))
        print(f"{endpoint}: {response_time:.4f}秒")
    
    average_time = sum(t for _, t in response_times) / len(response_times)
    print(f"平均响应时间: {average_time:.4f}秒")
    assert average_time < 1.0, f"平均响应时间超过1秒: {average_time:.4f}秒"

# 测试并发请求
def test_concurrent_requests():
    """测试并发请求处理能力"""
    def make_request():
        url = f"{BASE_URL}/api/datasource"
        response = requests.get(url)
        return response.status_code
    
    num_requests = 100
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    success_count = results.count(200)
    print(f"并发请求数: {num_requests}")
    print(f"成功响应数: {success_count}")
    print(f"成功率: {success_count/num_requests*100:.2f}%")
    assert success_count == num_requests, f"并发请求失败，成功数: {success_count}"

# 测试负载测试
def test_load_test():
    """测试系统负载能力"""
    url = f"{BASE_URL}/api/datasource"
    start_time = time.time()
    count = 0
    
    # 持续发送请求30秒
    while time.time() - start_time < 30:
        response = requests.get(url)
        if response.status_code == 200:
            count += 1
        time.sleep(0.1)  # 每100ms发送一次请求
    
    end_time = time.time()
    duration = end_time - start_time
    requests_per_second = count / duration
    
    print(f"测试持续时间: {duration:.2f}秒")
    print(f"成功请求数: {count}")
    print(f"每秒请求数: {requests_per_second:.2f}")
    assert count > 200, f"负载测试失败，请求数不足: {count}"

if __name__ == "__main__":
    print("=== 响应时间测试 ===")
    test_response_time()
    print("\n=== 并发请求测试 ===")
    test_concurrent_requests()
    print("\n=== 负载测试 ===")
    test_load_test()
    print("\n所有性能测试通过！")
