from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
from .models import CLTSubmission, CLTFile
from .serializers import (
    CLTSubmissionSerializer,
    CLTSubmissionCreateSerializer,
    CLTSubmissionUpdateSerializer,
    CLTFileSerializer
)


class CLTSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing CLT (Creative Learning Track) submissions.
    
    Supports:
    - List all submissions for current user
    - Create new submission with file uploads
    - Update submission details
    - Add files to existing submission
    - Submit for review
    - Retrieve submission status
    """
    
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        """Return submissions for current user only"""
        return CLTSubmission.objects.filter(user=self.request.user).prefetch_related('files')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return CLTSubmissionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CLTSubmissionUpdateSerializer
        return CLTSubmissionSerializer
    
    def create(self, request, *args, **kwargs):
        """Create new CLT submission"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()
        
        # Return full submission data
        response_serializer = CLTSubmissionSerializer(submission)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_files(self, request, pk=None):
        """
        Upload additional files to existing submission.
        POST /api/clt/{id}/upload_files/
        """
        submission = self.get_object()
        
        # Check if user owns this submission
        if submission.user != request.user:
            return Response(
                {'error': 'You do not have permission to modify this submission'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        files = request.FILES.getlist('files')
        if not files:
            return Response(
                {'error': 'No files provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_files = []
        for file in files:
            clt_file = CLTFile.objects.create(
                submission=submission,
                file=file,
                file_name=file.name,
                file_size=file.size,
                file_type=request.data.get('file_type', 'evidence')
            )
            created_files.append(clt_file)
        
        serializer = CLTFileSerializer(created_files, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Submit CLT submission for review.
        POST /api/clt/{id}/submit/
        """
        submission = self.get_object()
        
        # Check if user owns this submission
        if submission.user != request.user:
            return Response(
                {'error': 'You do not have permission to modify this submission'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validate submission is complete
        if not submission.title or not submission.description or not submission.platform or not submission.completion_date:
            return Response(
                {'error': 'Please complete all required fields before submitting'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not submission.files.exists():
            return Response(
                {'error': 'Please upload at least one file (certificate or evidence)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update submission status
        submission.status = 'submitted'
        submission.current_step = 3
        submission.submitted_at = timezone.now()
        submission.save()
        
        serializer = CLTSubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def delete_file(self, request, pk=None):
        """
        Delete a file from submission.
        DELETE /api/clt/{id}/delete_file/?file_id={file_id}
        """
        submission = self.get_object()
        
        # Check if user owns this submission
        if submission.user != request.user:
            return Response(
                {'error': 'You do not have permission to modify this submission'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        file_id = request.query_params.get('file_id')
        if not file_id:
            return Response(
                {'error': 'file_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            file_obj = CLTFile.objects.get(id=file_id, submission=submission)
            file_obj.file.delete()  # Delete actual file
            file_obj.delete()  # Delete database record
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CLTFile.DoesNotExist:
            return Response(
                {'error': 'File not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get submission statistics for current user.
        GET /api/clt/stats/
        """
        submissions = self.get_queryset()
        
        stats = {
            'total': submissions.count(),
            'draft': submissions.filter(status='draft').count(),
            'submitted': submissions.filter(status='submitted').count(),
            'under_review': submissions.filter(status='under_review').count(),
            'approved': submissions.filter(status='approved').count(),
            'rejected': submissions.filter(status='rejected').count(),
        }
        
        return Response(stats, status=status.HTTP_200_OK)
