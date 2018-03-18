SECRET_KEY = "ADLNASLDKN123!@#AS"
LOGGING_SECRET_KEY = "ADLNASLDKN123!@#ASASMFBASDBFKADSBNBSAJKDF"


class MongoCredentials:

  def __init__(self):
    self.host = URL().mongo_ip.split('http://')[1]
    self.port = URL().mongo_port
    self.db = "cons_stage"


class MYSQLCredentials:
  def __init__(self):
    self.url_obj = URL()
    self.host = self.url_obj.mysql_ip.split('http://')[1]
    self.port = self.url_obj.mysql_port
    self.db = "core"
    self.user = "root"
    self.password = "root"
    self.pool_recycle = 3600
    self.max_overflow = 5
    self.pool_size = 10
    self.pool_timeout = 30
    self.encoding = 'utf-8'
    self.mysql_url = 'mysql://{user}:{password}@{host}/{db}'.format(
      user=self.user,
      password=self.password,
      host=self.host,
      db=self.db
    )


class ElasticsearchCredentials:
  def __init__(self):
    url_obj = URL()
    self.host = url_obj.elastic_ip.split('http://')[1]
    self.port = url_obj.elastic_port
    self.index_names = {}
    self.load_index_names()

  def load_index_names(self):
    self.index_names = {
      'measures_missed': 'measure_master', 'risk': 'risk-master-new', 'medication': 'patient_master',
      'risk_hhs': 'risk-master-new', 'risk_cmscr': 'risk-master-new', 'ontology': 'ontology_master',
      'healthcare_codes': 'healthcare_codes', 'empi': 'empi_master', 'billings': 'patient_master',
      'clinical': 'patient_master', 'vitals': 'patient_master', 'personal_information': 'patient_master',
      'measures': 'measure_master', 'visits': 'patient_master', 'episodes': 'episode_master',
      'aco_org': 'aco_org_mstr', 'measure_operands': 'measure_master_operands', 'pcp': 'pcp_master',
      'attribution': 'attribution_master'
    }


class SparkContextConfiguration:
  def __init__(self):
    self.mem_per_node = '25G'
    self.num_cpu_cores = '4'
    self.spark_executors = '12'
    self.params = {'num-cpu-cores': self.num_cpu_cores, 'memory-per-node': self.mem_per_node,
                   'spark.executor.instances': self.spark_executors}

  def get_params(self):
    return self.params


class SharingPermissions:
  def __init__(self):
    self.permissions = ["can_view", "can_edit", "is_owner"]
    self.advanced_permissions = ["can_edit", "is_owner"]


class URL:
  def __init__(self):
    self.infra_url = "http://127.0.0.1"
    self.api_url = "http://127.0.0.1"
    self.elastic_ip = "http://127.0.0.1"
    self.mysql_ip = "http://127.0.0.1"
    self.mongo_ip = "http://127.0.0.1"
    self.redis_ip = "http://127.0.0.1"
    self.spark_ip = "http://rsm"
    self.workflow_ip = "http://as2"
    self.hdfs_ip = "http://pnn"
    self.phoenix_ip = "http://dn1"
    self.hbase_url = "http://snn"

    self.elastic_port = 9301
    self.mysql_port = 3306
    self.mongo_port = 27017
    self.redis_port = 6379
    self.spark_port = 8090
    self.workflow_port = [8585, 8089]
    self.hdfs_port = 50070
    self.phoenix_port = 20001
    self.api_port = 80
    self.hbase_port = 8180
