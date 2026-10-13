import pytest
import requests
import json

BASE_URL = "http://localhost:8000"

# 测试数据源平台
def test_datasource_creation():
    """测试数据源创建"""
    url = f"{BASE_URL}/api/datasource"
    data = {
        "name": "测试数据源",
        "type": "MYSQL",
        "host": "localhost",
        "port": 3306,
        "database": "test",
        "username": "root",
        "password": "123456"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "测试数据源"
    assert result["status"] == "CREATED"
    return result["id"]

def test_get_datasources():
    """测试获取数据源列表"""
    url = f"{BASE_URL}/api/datasource"
    response = requests.get(url)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)

def test_test_connection():
    """测试数据源连接测试"""
    url = f"{BASE_URL}/api/datasource/test"
    data = {
        "type": "MYSQL",
        "host": "localhost",
        "port": 3306,
        "database": "test",
        "username": "root",
        "password": "123456"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True

def test_execute_sql():
    """测试SQL执行"""
    url = f"{BASE_URL}/api/datasource/execute"
    data = {
        "datasourceId": 1,
        "sql": "SELECT * FROM test",
        "limit": 100
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert "columns" in result
    assert "rows" in result

# 测试数据库同步平台
def test_sync_task_creation():
    """测试同步任务创建"""
    url = f"{BASE_URL}/api/sync/task"
    data = {
        "name": "测试同步任务",
        "sourceId": 1,
        "targetId": 2,
        "syncType": "FULL",
        "syncStrategy": {
            "tables": ["test1", "test2"],
            "columns": {"test1": ["id", "name"]}
        }
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "测试同步任务"
    assert result["status"] == "CREATED"
    return result["id"]

def test_start_sync_task():
    """测试同步任务启动"""
    task_id = test_sync_task_creation()
    url = f"{BASE_URL}/api/sync/task/{task_id}/start"
    response = requests.post(url)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == task_id
    assert result["status"] == "RUNNING"

def test_get_sync_task_status():
    """测试同步任务状态查询"""
    task_id = test_sync_task_creation()
    url = f"{BASE_URL}/api/sync/task/{task_id}/status"
    response = requests.get(url)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == task_id
    assert "status" in result
    assert "progress" in result
    assert "logs" in result

# 测试数据存储平台
def test_cluster_creation():
    """测试集群创建"""
    url = f"{BASE_URL}/api/storage/cluster"
    data = {
        "name": "测试集群",
        "type": "HDFS",
        "config": {
            "namenode": "localhost:9000",
            "datanode": ["localhost:9001", "localhost:9002"]
        }
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "测试集群"
    assert result["status"] == "CREATED"
    return result["id"]

def test_cluster_monitor():
    """测试集群监控"""
    cluster_id = test_cluster_creation()
    url = f"{BASE_URL}/api/storage/cluster/{cluster_id}/monitor"
    response = requests.get(url)
    assert response.status_code == 200
    result = response.json()
    assert result["cluster_id"] == cluster_id
    assert "cpu_usage" in result
    assert "memory_usage" in result

def test_storage_policy_creation():
    """测试存储策略创建"""
    url = f"{BASE_URL}/api/storage/policy"
    data = {
        "name": "测试存储策略",
        "type": "HOT",
        "rules": {
            "retention": "30d",
            "compression": "gzip"
        }
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "测试存储策略"
    assert result["status"] == "ACTIVE"

# 测试数据汇聚平台
def test_connector_creation():
    """测试连接器创建"""
    url = f"{BASE_URL}/api/汇聚/connector"
    data = {
        "name": "测试连接器",
        "type": "JDBC",
        "config": {
            "url": "jdbc:mysql://localhost:3306/test",
            "username": "root",
            "password": "123456"
        }
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "测试连接器"
    assert result["status"] == "ACTIVE"
    return result["id"]

def test_etl_task_creation():
    """测试ETL任务创建"""
    url = f"{BASE_URL}/api/汇聚/etl/task"
    data = {
        "name": "测试ETL任务",
        "source_connector_id": 1,
        "target_connector_id": 2,
        "transformation_rules": [
            {"type": "SELECT", "columns": ["id", "name"]},
            {"type": "FILTER", "condition": "id > 10"}
        ],
        "schedule": "0 0 * * *"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "测试ETL任务"
    assert result["status"] == "CREATED"
    return result["id"]

def test_start_etl_task():
    """测试ETL任务启动"""
    task_id = test_etl_task_creation()
    url = f"{BASE_URL}/api/汇聚/etl/task/{task_id}/start"
    response = requests.post(url)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == task_id
    assert result["status"] == "RUNNING"

# 测试数据中枢平台
def test_metadata_creation():
    """测试元数据创建"""
    url = f"{BASE_URL}/api/中枢/metadata"
    data = {
        "name": "测试表",
        "type": "TABLE",
        "description": "测试表描述",
        "attributes": {
            "owner": "admin",
            "create_time": "2026-03-12"
        }
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "测试表"
    return result["id"]

def test_get_lineage():
    """测试数据血缘查询"""
    metadata_id = test_metadata_creation()
    url = f"{BASE_URL}/api/中枢/lineage/{metadata_id}"
    response = requests.get(url)
    assert response.status_code == 200
    result = response.json()
    assert "nodes" in result
    assert "edges" in result

def test_get_quality_check():
    """测试数据质量检查"""
    asset_id = 1
    url = f"{BASE_URL}/api/中枢/quality/{asset_id}"
    response = requests.get(url)
    assert response.status_code == 200
    result = response.json()
    assert result["asset_id"] == asset_id
    assert "check_results" in result
    assert "overall_score" in result

# 测试数据分析平台
def test_cube_creation():
    """测试立方体创建"""
    url = f"{BASE_URL}/api/分析/cube"
    data = {
        "name": "测试立方体",
        "dimensions": ["date", "region"],
        "measures": ["sales", "profit"],
        "source_table": "sales_table"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "测试立方体"
    assert result["status"] == "CREATED"
    return result["id"]

def test_execute_query():
    """测试SQL查询执行"""
    url = f"{BASE_URL}/api/分析/query"
    data = {
        "sql": "SELECT * FROM sales_table",
        "limit": 100
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert "columns" in result
    assert "rows" in result
    assert "total" in result
    assert "execution_time" in result

# 测试数据开发平台
def test_stream_job_creation():
    """测试流处理作业创建"""
    url = f"{BASE_URL}/api/开发/stream/job"
    data = {
        "name": "测试流处理作业",
        "type": "FLINK",
        "code": "// Flink作业代码",
        "config": {
            "parallelism": 2,
            "checkpoint_interval": "10s"
        }
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "测试流处理作业"
    assert result["status"] == "CREATED"
    return result["id"]

def test_start_stream_job():
    """测试流处理作业启动"""
    job_id = test_stream_job_creation()
    url = f"{BASE_URL}/api/开发/stream/job/{job_id}/start"
    response = requests.post(url)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == job_id
    assert result["status"] == "RUNNING"

# 测试统一服务层
def test_api_creation():
    """测试API创建"""
    url = f"{BASE_URL}/api/service/api"
    data = {
        "name": "测试API",
        "url": "/api/test",
        "method": "GET",
        "params": {
            "id": "int",
            "name": "string"
        }
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "测试API"
    assert result["status"] == "ACTIVE"

def test_user_creation():
    """测试用户创建"""
    url = f"{BASE_URL}/api/service/user"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "role": "user",
        "password": "123456"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "testuser"
    assert result["role"] == "user"

def test_get_monitor():
    """测试系统监控"""
    url = f"{BASE_URL}/api/service/monitor"
    response = requests.get(url)
    assert response.status_code == 200
    result = response.json()
    assert "system_status" in result
    assert "components" in result
    assert "metrics" in result

# 测试健康检查
def test_health_check():
    """测试健康检查"""
    url = f"{BASE_URL}/health"
    response = requests.get(url)
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "healthy"

if __name__ == "__main__":
    # 运行所有测试
    test_datasource_creation()
    test_get_datasources()
    test_test_connection()
    test_execute_sql()
    test_sync_task_creation()
    test_start_sync_task()
    test_get_sync_task_status()
    test_cluster_creation()
    test_cluster_monitor()
    test_storage_policy_creation()
    test_connector_creation()
    test_etl_task_creation()
    test_start_etl_task()
    test_metadata_creation()
    test_get_lineage()
    test_get_quality_check()
    test_cube_creation()
    test_execute_query()
    test_stream_job_creation()
    test_start_stream_job()
    test_api_creation()
    test_user_creation()
    test_get_monitor()
    test_health_check()
    print("所有测试通过！")
