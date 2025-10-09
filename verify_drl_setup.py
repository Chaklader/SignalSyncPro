"""
Verification script to check DRL implementation setup
"""
import sys
import os

def check_imports():
    """Check if all required packages can be imported"""
    print("Checking Python packages...")
    
    packages = {
        'torch': 'PyTorch',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'matplotlib': 'Matplotlib',
        'yaml': 'PyYAML',
        'tqdm': 'tqdm'
    }
    
    missing = []
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT FOUND")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements_drl.txt")
        return False
    return True

def check_sumo():
    """Check if SUMO is available"""
    print("\nChecking SUMO installation...")
    
    if 'SUMO_HOME' not in os.environ:
        print("  ✗ SUMO_HOME environment variable not set")
        return False
    
    print(f"  ✓ SUMO_HOME: {os.environ['SUMO_HOME']}")
    
    # Add SUMO tools to path
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    if tools not in sys.path:
        sys.path.append(tools)
    
    try:
        import traci
        print("  ✓ TraCI module")
        return True
    except ImportError:
        print("  ✗ TraCI module not found")
        print(f"     Tried: {tools}")
        return False

def check_drl_modules():
    """Check if DRL modules can be imported"""
    print("\nChecking DRL modules...")
    
    modules = [
        'drl.config',
        'drl.neural_network',
        'drl.replay_buffer',
        'drl.reward',
        'drl.environment',
        'drl.agent'
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except Exception as e:
            print(f"  ✗ {module} - {str(e)}")
            all_ok = False
    
    return all_ok

def check_existing_infrastructure():
    """Check if existing SignalSyncPro files are present"""
    print("\nChecking existing infrastructure...")
    
    files = [
        'constants.py',
        'tls_constants.py',
        'detectors.py',
        'common.py',
        'test.sumocfg',
        'infrastructure/developed/network/test.net.xml'
    ]
    
    all_ok = True
    for file in files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - NOT FOUND")
            all_ok = False
    
    return all_ok

def check_directories():
    """Check if required directories exist"""
    print("\nChecking directories...")
    
    dirs = [
        'drl',
        'training',
        'testing',
        'models',
        'logs',
        'results'
    ]
    
    all_ok = True
    for dir in dirs:
        if os.path.isdir(dir):
            print(f"  ✓ {dir}/")
        else:
            print(f"  ✗ {dir}/ - NOT FOUND")
            all_ok = False
    
    return all_ok

def test_environment_creation():
    """Test if environment can be created"""
    print("\nTesting environment creation...")
    
    try:
        from drl.traffic_management import TrafficManagement
        from drl.config import DRLConfig
        
        # Try to create environment (won't start SUMO)
        env = TrafficManagement("test.sumocfg", ['3', '6'], gui=False)
        print("  ✓ Environment object created")
        
        # Check state dimension
        print(f"  ✓ Action dimension: {DRLConfig.ACTION_DIM}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False

def test_agent_creation():
    """Test if agent can be created"""
    print("\nTesting agent creation...")
    
    try:
        from drl.agent import DQNAgent
        
        # Create agent with dummy dimensions
        agent = DQNAgent(state_dim=45, action_dim=4)
        print("  ✓ Agent created")
        print(f"  ✓ Device: {agent.device}")
        print(f"  ✓ Policy network parameters: {sum(p.numel() for p in agent.policy_net.parameters()):,}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False

def main():
    """Run all verification checks"""
    print("="*60)
    print("DRL Implementation Verification")
    print("="*60)
    
    checks = [
        ("Python Packages", check_imports),
        ("SUMO Installation", check_sumo),
        ("DRL Modules", check_drl_modules),
        ("Existing Infrastructure", check_existing_infrastructure),
        ("Directories", check_directories),
        ("Environment Creation", test_environment_creation),
        ("Agent Creation", test_agent_creation)
    ]
    
    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 All checks passed! DRL implementation is ready to use.")
        print("\nNext steps:")
        print("  1. Generate route files:")
        print("     python privateCarRouteFile.py")
        print("     python bicycleRouteFile.py")
        print("     python pedestrianRouteFile.py")
        print("  2. Start training:")
        print("     ./run_training.sh")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("  - Install packages: pip install -r requirements_drl.txt")
        print("  - Set SUMO_HOME: export SUMO_HOME=/path/to/sumo")
        print("  - Check file paths and directory structure")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
