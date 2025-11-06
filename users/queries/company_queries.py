import graphene
from graphene import ObjectType
from users.company_models import Company, Address
from users.types.company_node import CompanyNode, AddressNode


class CompanyQueries(ObjectType):
    """Company related queries"""
    
    # Get current user's company profile
    my_company_profile = graphene.Field(CompanyNode)
    
    # Get a company by ID
    company = graphene.Field(
        CompanyNode,
        id=graphene.ID(required=True)
    )
    
    # Get a company by user ID
    company_by_user = graphene.Field(
        CompanyNode,
        user_id=graphene.ID(required=True)
    )
    
    # List all companies (with pagination)
    companies = graphene.List(
        CompanyNode,
        first=graphene.Int(default_value=10),
        skip=graphene.Int(default_value=0),
        domain_activity=graphene.String(),
        size=graphene.String(),
        country=graphene.String(),
        disponibilite_collaboration=graphene.String()
    )
    
    # Get companies count
    companies_count = graphene.Int(
        domain_activity=graphene.String(),
        size=graphene.String(),
        country=graphene.String(),
        disponibilite_collaboration=graphene.String()
    )
    
    def resolve_my_company_profile(self, info):
        """Get the authenticated user's company profile"""
        user = info.context.user
        
        if not user.is_authenticated:
            return None
        
        if not hasattr(user, 'company_profile'):
            return None
        
        return user.company_profile
    
    def resolve_company(self, info, id):
        """Get a specific company by ID"""
        try:
            return Company.objects.select_related('user', 'address').get(id=id)
        except Company.DoesNotExist:
            return None
    
    def resolve_company_by_user(self, info, user_id):
        """Get a company profile by user ID"""
        try:
            return Company.objects.select_related('user', 'address').get(user_id=user_id)
        except Company.DoesNotExist:
            return None
    
    def resolve_companies(self, info, first=10, skip=0, **filters):
        """List companies with optional filters"""
        queryset = Company.objects.select_related('user', 'address').all()
        
        # Apply filters
        if filters.get('domain_activity'):
            queryset = queryset.filter(domain_activity=filters['domain_activity'])
        
        if filters.get('size'):
            queryset = queryset.filter(size=filters['size'])
        
        if filters.get('disponibilite_collaboration'):
            queryset = queryset.filter(disponibilite_collaboration=filters['disponibilite_collaboration'])
        
        if filters.get('country'):
            queryset = queryset.filter(address__country=filters['country'])
        
        # Apply pagination
        return queryset[skip:skip + first]
    
    def resolve_companies_count(self, info, **filters):
        """Get the count of companies with optional filters"""
        queryset = Company.objects.all()
        
        # Apply filters
        if filters.get('domain_activity'):
            queryset = queryset.filter(domain_activity=filters['domain_activity'])
        
        if filters.get('size'):
            queryset = queryset.filter(size=filters['size'])
        
        if filters.get('disponibilite_collaboration'):
            queryset = queryset.filter(disponibilite_collaboration=filters['disponibilite_collaboration'])
        
        if filters.get('country'):
            queryset = queryset.filter(address__country=filters['country'])
        
        return queryset.count()
