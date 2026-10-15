"""Read-only AWS checks against identifiers recorded during this actual lab."""
from pathlib import Path
import datetime,json,subprocess
project=Path(__file__).resolve().parents[2]
live=json.loads((project/'Output/reports/aws-live-resources.json').read_text())
def aws(*args):
    return json.loads(subprocess.check_output(['aws',*args,'--profile','scaler-sst','--region','ap-southeast-2','--output','json'],text=True))
assert aws('sts','get-caller-identity')['Account']==live['account']=='499567237930'
vpc=live['vpc'][0]['VpcId'];cluster=live['cluster']['name'];lb=live['load_balancer']['LoadBalancerName']
volumes=sorted({live['database_volume']['VolumeId']} | {b['Ebs']['VolumeId'] for r in live['worker_instances']['Reservations'] for i in r['Instances'] for b in i['BlockDeviceMappings']})
checks={}
checks['cluster_absent']=cluster not in aws('eks','list-clusters')['clusters']
checks['vpc_absent']=not aws('ec2','describe-vpcs','--filters',f'Name=vpc-id,Values={vpc}')['Vpcs']
checks['subnets_absent']=not aws('ec2','describe-subnets','--filters',f'Name=vpc-id,Values={vpc}')['Subnets']
checks['security_groups_absent']=not aws('ec2','describe-security-groups','--filters',f'Name=vpc-id,Values={vpc}')['SecurityGroups']
checks['network_interfaces_absent']=not aws('ec2','describe-network-interfaces','--filters',f'Name=vpc-id,Values={vpc}')['NetworkInterfaces']
checks['recorded_volumes_absent']=not aws('ec2','describe-volumes','--filters','Name=volume-id,Values='+','.join(volumes))['Volumes']
checks['load_balancer_absent']=not [x for x in aws('elb','describe-load-balancers')['LoadBalancerDescriptions'] if x['LoadBalancerName']==lb]
instances=aws('ec2','describe-instances','--instance-ids',*live['worker_instance_ids'])
worker_states={i['InstanceId']:i['State']['Name'] for r in instances['Reservations'] for i in r['Instances']}
checks['worker_terminated']=bool(worker_states) and all(s=='terminated' for s in worker_states.values())
roles=aws('iam','list-roles')['Roles']
expected_roles={live['cluster']['roleArn'].split('/')[-1],live['nodegroup']['nodeRole'].split('/')[-1],'labledger-session21-ebs-csi'}
checks['project_iam_roles_absent']=not any(r['RoleName'] in expected_roles for r in roles)
state=subprocess.check_output(['terraform','-chdir=terraform','state','list'],cwd=project,text=True).strip()
checks['terraform_state_empty']=not state
buckets={b['Name'] for b in aws('s3api','list-buckets')['Buckets']}
checks['session18_bucket_absent']='devops-session18-499567237930-20261015' not in buckets
checks['session19_bucket_absent']='devops-session19-499567237930-20261015' not in buckets
checks['session19_vpc_absent']=not aws('ec2','describe-vpcs','--filters','Name=vpc-id,Values=vpc-028b9710ea8609a72')['Vpcs']
s19=aws('ec2','describe-instances','--instance-ids','i-0522f5d4ea618a6f5','i-07925ab838a87caa0')
checks['session19_instances_terminated']=all(i['State']['Name']=='terminated' for r in s19['Reservations'] for i in r['Instances'])
preserved=aws('eks','describe-cluster','--name','scaler-sst-taskboard')['cluster']['status']
checks['earlier_taskboard_cluster_preserved']=preserved=='ACTIVE'
record={'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'account':live['account'],'region':live['region'],'target_cluster':cluster,'target_vpc':vpc,'recorded_worker_states':worker_states,'recorded_volume_ids':volumes,'target_load_balancer':lb,'checks':checks,'all_checks_passed':all(checks.values()),'earlier_taskboard_status':preserved}
(project/'Output/reports/aws-cleanup-verification.json').write_text(json.dumps(record,indent=2)+'\n')
for label,passed in checks.items():print(('PASS' if passed else 'FAIL')+' '+label)
assert record['all_checks_passed'],record
print('ALL AWS CLEANUP CHECKS PASSED; earlier TaskBoard cluster remains ACTIVE')
