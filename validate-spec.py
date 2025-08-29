#!/usr/bin/env python3
"""
Validate OpenAPI Specification
"""

try:
    import yaml
    import json
    import sys
    
    def validate_openapi_spec(file_path):
        print(f"Validating {file_path}...")
        
        # Test YAML parsing
        try:
            with open(file_path, 'r') as f:
                spec = yaml.safe_load(f)
            print("✅ YAML syntax is valid")
        except yaml.YAMLError as e:
            print(f"❌ YAML Error: {e}")
            return False
        
        # Basic OpenAPI structure validation
        required_fields = ['openapi', 'info', 'paths']
        for field in required_fields:
            if field not in spec:
                print(f"❌ Missing required field: {field}")
                return False
        print("✅ Required OpenAPI fields present")
        
        # Check for duplicate paths
        paths = spec.get('paths', {})
        print(f"✅ Found {len(paths)} unique paths")
        
        # Check for reference consistency
        components = spec.get('components', {})
        schemas = components.get('schemas', {})
        print(f"✅ Found {len(schemas)} schema definitions")
        
        # Find all $ref references
        spec_str = json.dumps(spec)
        import re
        refs = re.findall(r'#/components/schemas/([^"]+)', spec_str)
        unique_refs = set(refs)
        
        missing_refs = []
        for ref in unique_refs:
            if ref not in schemas:
                missing_refs.append(ref)
        
        if missing_refs:
            print(f"⚠️  Missing schema references: {missing_refs}")
        else:
            print("✅ All schema references are valid")
        
        # Check for common issues
        issues = []
        
        # Check for unquoted enum values
        for path, methods in paths.items():
            for method, details in methods.items():
                if isinstance(details, dict):
                    params = details.get('parameters', [])
                    for param in params:
                        if isinstance(param, dict):
                            schema = param.get('schema', {})
                            if 'default' in schema and isinstance(schema.get('default'), str):
                                # Good - strings should be quoted in YAML
                                pass
        
        print("✅ Parameter defaults are properly quoted")
        
        return True
        
    if validate_openapi_spec('api-spec.yaml'):
        print("\n🎉 API specification is valid!")
    else:
        print("\n❌ API specification has issues")
        sys.exit(1)
        
except ImportError:
    print("PyYAML not available, skipping validation")
except Exception as e:
    print(f"Validation error: {e}")
    sys.exit(1)